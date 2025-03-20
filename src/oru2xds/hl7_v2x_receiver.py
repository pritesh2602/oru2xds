#!/usr/bin/env python3
#
# Antonio Martins (digiplan.pt@gmail.com)
#

import os
import logging
import aiorun
import hl7
import asyncio
from hl7.mllp import start_hl7_server

import config
###################################################################


# Logging facility
logger = logging.getLogger(config.APP_NAME + "." + __name__)


###################################################################
## Class Hl7v2x
###################################################################


class Hl7v2x:
	def __init__(self) -> None:
		pass

	#
	## Shows all patient ID domains
	## If none matches the XAD-PID, then bail-out
	#
	def show_all_pid_domains(self, hl7message):
		matching_domain_repetition = 0
		pid3_repetitions = len(hl7message.segment('PID')(3))
		logger.info("HL7 PID-3 has %s repetitions", pid3_repetitions)
		for repetition in range(1, pid3_repetitions + 1):
			# logger.debug("    Assigning authority OID: {}".format(hl7message.unescape(str(hl7message.segment('PID')(3)(repetition)(4)(2)))))
			logger.debug("    PID-3.%s: %s", repetition, hl7message.segment('PID')(3)(repetition))
			if hl7message.unescape(str(hl7message.segment('PID')(3)(repetition)(4)(2))) == config.AFFINITY_DOMAIN_ASSIGNING_AUTHORITY_OID:
				matching_domain_repetition = repetition
				
		if matching_domain_repetition == 0:
			raise RuntimeError("no PID-3 repetition matches the XDS affinity domain assigning authority OID. {}".format(config.AFFINITY_DOMAIN_ASSIGNING_AUTHORITY_OID))
		return matching_domain_repetition


	#
	## Verifies that all domains have an Universal Id Type (PID-3.4.3) as OID or ISO
	#
	def checkUniversalIdType(self, hl7message):
		universal_id_types = {'DNS', 'GUID', 'HCD', 'HL7', 'ISO', 'L', 'M', 'N', 'Random', 'URI', 'UUID', 'x400', 'x500'}
		for repetition in range(1, len(hl7message.segment('PID')(3)) + 1):
			if hl7message.segment('PID')(3)(repetition)(4)(3) not in universal_id_types:
				logger.error("Universal ID Type not present in PID-3.%s.4.3", repetition)
				# We could set it to ISO, but we are not doing that
				# hl7message['PID.3.{}.4.3'.format(repetition)] = "ISO"
				raise RuntimeError("Universal ID Type not present in PID-3.{}.4.3".format(repetition))


	#
	## Chooses the patient ID that matches the XAD-PID and returns
	## the repetition in PID segment that corresponds
	#
	@classmethod
	def hl7_find_xad_pid_repetition(self, hl7message):
		for repetition in range(1, len(hl7message.segment('PID')(3)) + 1):
			if hl7message.segment('PID')(3)(repetition)(4)(2) == config.AFFINITY_DOMAIN_ASSIGNING_AUTHORITY_OID:
				return repetition
		raise RuntimeError("no PID-3 repetition matches the XDS affinity domain assigning authority OID. {}".format(config.AFFINITY_DOMAIN_ASSIGNING_AUTHORITY_OID))


	#
	## Processes each HL7 message and calls the CDA converter
	# Adapted from https://python-hl7.readthedocs.io/en/latest/mllp.html
	#
	async def process_hl7_message(self, hl7_reader, hl7_writer):
		from ihe_xds import IheXds  # Delayed import to resolve circular dependency
		peername = hl7_writer.get_extra_info("peername")
		logger.info("Connection established %s", peername)
		try:
			# We're going to keep listening until the writer
			# is closed. Only writers have closed status.
			while not hl7_writer.is_closing():
				hl7_message = await hl7_reader.readmessage()
				try:
					logger.info("HL7 message received")
					logger.debug("Received HL7 message{}{}".format(os.linesep, f'{hl7_message}'.replace('\r', os.linesep)))
					self.show_all_pid_domains(hl7_message)
					# This call makes sure that PID-3.4.3 is ISO or OID
					self.checkUniversalIdType(hl7_message)
					# Convert the HL7 message into a full ProvideAndRegisterDocumentSetRequest
					# This means converting int a CDA inside a ProvideAndRegisterDocumentSetRequest,
					# then sent as a SOAP, and processing the response
					xds = IheXds()
					xds.convert_to_ITI41(hl7_message)
				# Send ACK and wait for the writer to drain
				except RuntimeError as err:
					# NACK
					logger.info("Sending back HL7 NACK")
					logger.info("NACK error will be %s", err)
					return_message = hl7_message.create_ack(ack_code = "AE", application = config.HL7_MY_SENDING_APP,
						facility = config.HL7_MY_SENDING_FACILITY)
					# Length of the answer in MSA-3 should be up to 80 characters
					return_message['MSA.F3'] = str(err)[0:77] + "..."
					return_message.escape('MSA.F3')
				else:
					# ACK
					logger.info("Sending back HL7 ACK")
					return_message = hl7_message.create_ack(application = config.HL7_MY_SENDING_APP,
						facility = config.HL7_MY_SENDING_FACILITY)
				logger.debug(return_message)
				hl7_writer.writemessage(return_message)
				await hl7_writer.drain()
		except asyncio.IncompleteReadError:
			# Oops, something went wrong, if the writer is not
			# closed or closing, close it.
			if not hl7_writer.is_closing():
				hl7_writer.close()
				await hl7_writer.wait_closed()
		logger.info("Connection closed %s", peername)


	#
	## Creates an HL7 server service
	# Adapted from https://python-hl7.readthedocs.io/en/latest/mllp.html
	#
	async def start_server(self):
		try:
			# Start the server in a with clause to make sure we close it
			logger.info("Starting HL7 receiver on port %s", config.HL7_LISTENER_PORT)
			async with await start_hl7_server(
				self.process_hl7_message,
				port = config.HL7_LISTENER_PORT, encoding = "UTF-8"
			) as hl7_server:
				# And now we serve forever. Or until we are cancelled...
				await hl7_server.serve_forever()
		except asyncio.CancelledError:
			# Cancelled errors are expected
			pass


	#
	## Start the HL7 MLLP receive service
	#
	def start_service(self):
		aiorun.run(self.start_server(), stop_on_unhandled_errors = True)
