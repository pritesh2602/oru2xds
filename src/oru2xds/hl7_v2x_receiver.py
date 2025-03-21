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

# Logging facility
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(f"{config.APP_NAME}.{__name__}")

class Hl7v2x:
    def __init__(self) -> None:
        pass

    def show_all_pid_domains(self, hl7message):
        matching_domain_repetition = 0
        pid3_repetitions = len(hl7message.segment('PID')(3))
        logger.info("HL7 PID-3 has %s repetitions", pid3_repetitions)
        for repetition in range(1, pid3_repetitions + 1):
            logger.debug("    PID-3.%s: %s", repetition, hl7message.segment('PID')(3)(repetition))
            if hl7message.unescape(str(hl7message.segment('PID')(3)(repetition)(4)(2))) == config.AFFINITY_DOMAIN_ASSIGNING_AUTHORITY_OID:
                matching_domain_repetition = repetition

        if matching_domain_repetition == 0:
            raise RuntimeError(f"no PID-3 repetition matches the XDS affinity domain assigning authority OID. {config.AFFINITY_DOMAIN_ASSIGNING_AUTHORITY_OID}")
        return matching_domain_repetition

    def check_universal_id_type(self, hl7message):
        universal_id_types = {'DNS', 'GUID', 'HCD', 'HL7', 'ISO', 'L', 'M', 'N', 'Random', 'URI', 'UUID', 'x400', 'x500'}
        for repetition in range(1, len(hl7message.segment('PID')(3)) + 1):
            if hl7message.segment('PID')(3)(repetition)(4)(3) not in universal_id_types:
                logger.error("Universal ID Type not present in PID-3.%s.4.3", repetition)
                raise RuntimeError(f"Universal ID Type not present in PID-3.{repetition}.4.3")

    @classmethod
    def hl7_find_xad_pid_repetition(cls, hl7message):
        for repetition in range(1, len(hl7message.segment('PID')(3)) + 1):
            if hl7message.segment('PID')(3)(repetition)(4)(2) == config.AFFINITY_DOMAIN_ASSIGNING_AUTHORITY_OID:
                return repetition
        raise RuntimeError(f"no PID-3 repetition matches the XDS affinity domain assigning authority OID. {config.AFFINITY_DOMAIN_ASSIGNING_AUTHORITY_OID}")

    async def process_hl7_message(self, hl7_reader, hl7_writer):
        from ihe_xds import IheXds  # Local import to avoid circular dependency

        peername = hl7_writer.get_extra_info("peername")
        logger.info("Connection established with %s", peername)
        try:
            while not hl7_writer.is_closing():
                hl7_message = await hl7_reader.readmessage()
                try:
                    logger.info("HL7 message received")
                    logger.debug("Received HL7 message:{}{}".format(os.linesep, f'{hl7_message}'.replace('\r', os.linesep)))
                    self.show_all_pid_domains(hl7_message)
                    self.check_universal_id_type(hl7_message)
                    xds = IheXds()
                    xds.convert_to_ITI41(hl7_message)
                    logger.info("Sending back HL7 ACK")
                    return_message = hl7_message.create_ack(application=config.HL7_MY_SENDING_APP,
                                                            facility=config.HL7_MY_SENDING_FACILITY)
                except RuntimeError as err:
                    logger.error("Error processing HL7 message: %s", err)
                    logger.info("Sending back HL7 NACK")
                    return_message = hl7_message.create_ack(ack_code="AE", application=config.HL7_MY_SENDING_APP,
                                                            facility=config.HL7_MY_SENDING_FACILITY)
                    return_message['MSA.F3'] = str(err)[:77] + "..."
                    return_message.escape('MSA.F3')
                except Exception as e:
                    logger.exception("Unexpected error occurred: %s", e)
                    raise
                finally:
                    logger.debug("Returning message: %s", return_message)
                    hl7_writer.writemessage(return_message)
                    await hl7_writer.drain()
        except asyncio.IncompleteReadError:
            logger.warning("Connection closed by client: %s", peername)
        except Exception as e:
            logger.exception("Unexpected error in connection with %s: %s", peername, e)
        finally:
            if not hl7_writer.is_closing():
                hl7_writer.close()
                await hl7_writer.wait_closed()
            logger.info("Connection closed with %s", peername)

    async def start_server(self):
        try:
            logger.info("Starting HL7 receiver on port %s", config.HL7_LISTENER_PORT)
            async with await start_hl7_server(
                self.process_hl7_message,
                port=config.HL7_LISTENER_PORT, encoding="UTF-8"
            ) as hl7_server:
                logger.info("HL7 server started successfully.")
                await hl7_server.serve_forever()
        except asyncio.CancelledError:
            logger.info("HL7 server shutdown requested.")
        except Exception as e:
            logger.exception("Unexpected error in HL7 server: %s", e)

    def start_service(self):
        logger.info("Starting HL7 service...")
        try:
            aiorun.run(self.start_server(), stop_on_unhandled_errors=True)
        except Exception as e:
            logger.exception("Failed to start HL7 service: %s", e)

if __name__ == "__main__":
    receiver = Hl7v2x()
    receiver.start_service()