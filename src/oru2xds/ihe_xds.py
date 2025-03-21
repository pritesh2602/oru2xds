#!/usr/bin/python3
#
# Antonio Martins (digiplan.pt@gmail.com)
#

import os
import logging
import uuid
from lxml import etree
from lxml.builder import ElementMaker
import hl7
from sympy import false
import config
import hl7_v2x_receiver
from hl7_cda import HL7CdaBuilder
from soap import SOAP


###################################################################


# Logging facility
logger = logging.getLogger(config.APP_NAME + "." + __name__)

# Define namespaces
NSMAP = {
	'soapenv': 'http://www.w3.org/2003/05/soap-envelope',
	'wsa': 'http://www.w3.org/2005/08/addressing',
	'xdsb': 'urn:ihe:iti:xds-b:2007',
	'lcm': 'urn:oasis:names:tc:ebxml-regrep:xsd:lcm:3.0',
	'rim': 'urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0',
	'xop': 'http://www.w3.org/2004/08/xop/include',
	'rs' : "urn:oasis:names:tc:ebxml-regrep:xsd:rs:3.0"}
nsmap_xdsb = {
	'xdsb': 'urn:ihe:iti:xds-b:2007'}
xdsb_prefix = "{" + nsmap_xdsb['xdsb'] + "}"
nsmap_lcm =  {
	'lcm': 'urn:oasis:names:tc:ebxml-regrep:xsd:lcm:3.0'}
lcm_prefix = "{" + nsmap_lcm['lcm'] + "}"
nsmap_rim =  {
	'rim': 'urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0'}
rim_prefix = "{" + nsmap_rim['rim'] + "}"
nsmap_xop = {
	'xop': 'http://www.w3.org/2004/08/xop/include'}
xop_prefix = "{" + nsmap_xop['xop'] + "}"

object_symbolic_id = None


###################################################################
## class IheXds
###################################################################


class IheXds:
	def __init__(self):
		self.object_symbolic_id = 0

		self.m_DocumentEntry_author = None
		self.m_DocumentEntry_availabilityStatus = None
		self.m_DocumentEntry_classCode = None
		self.m_DocumentEntry_comments = None
		self.m_DocumentEntry_confidentialityCode = None
		self.m_DocumentEntry_creationTime = None
		self.m_DocumentEntry_entryUUID = None
		self.m_DocumentEntry_eventCodeList = None
		self.m_DocumentEntry_formatCode = None
		self.m_DocumentEntry_healthcareFacilityTypeCode = None
		self.m_DocumentEntry_homeCommunityId = None
		self.m_DocumentEntry_languageCode = None
		self.m_DocumentEntry_legalAuthenticator = None
		self.m_DocumentEntry_mimeType = None
		self.m_DocumentEntry_objectType = None
		self.m_DocumentEntry_patientId = None
		self.m_DocumentEntry_practiceSettingCode = None
		self.m_DocumentEntry_referenceIdList = None
		self.m_DocumentEntry_repositoryUniqueId = None
		self.m_DocumentEntry_serviceStartTime = None
		self.m_DocumentEntry_serviceStopTime = None
		self.m_DocumentEntry_sourcePatientId = None
		self.m_DocumentEntry_sourcePatientInfo = None
		self.m_DocumentEntry_title = None
		self.m_DocumentEntry_typeCode = None
		self.m_DocumentEntry_uniqueId = None
		self.m_DocumentEntry_URI = None

		self.m_SubmissionSet_author = None
		self.m_SubmissionSet_comments = None
		self.m_SubmissionSet_contentTypeCode = None
		self.m_SubmissionSet_entryUUID = None
		self.m_SubmissionSet_homeCommunityId = None
		self.m_SubmissionSet_intendedRecipient = None
		self.m_SubmissionSet_patientId = None
		self.m_SubmissionSet_sourceId = None
		self.m_SubmissionSet_submissionTime = None
		self.m_SubmissionSet_title = None
		self.m_SubmissionSet_uniqueId = None

		self.m_SubmissionSet_author = None
		self.m_SubmissionSet_comments = None
		self.m_SubmissionSet_contentTypeCode = None
		self.m_SubmissionSet_entryUUID = None
		self.m_SubmissionSet_homeCommunityId = None
		self.m_SubmissionSet_intendedRecipient = None
		self.m_SubmissionSet_patientId = None
		self.m_SubmissionSet_sourceId = None
		self.m_SubmissionSet_submissionTime = None
		self.m_SubmissionSet_title = None
		self.m_SubmissionSet_uniqueId = None


###################################################################
## Main configuration
###################################################################


	# These are the following fields that should go into an XDS document submission request
	# Metadata Element 	Metadata Attribute 	XDS DS
	# DocumentEntry		author					R2
	# DocumentEntry		availabilityStatus		O
	# DocumentEntry		classCode				R
	# DocumentEntry		comments				O
	# DocumentEntry		confidentialityCode		R
	# DocumentEntry		creationTime			R
	# DocumentEntry		entryUUID				R
	# DocumentEntry		eventCodeList			O
	# DocumentEntry		formatCode				R
	# DocumentEntry		hash					O
	# DocumentEntry		healthcareFacilityTypeCode		R
	# DocumentEntry		homeCommunityId			O
	# DocumentEntry		languageCode			R
	# DocumentEntry		legalAuthenticator		O
	# DocumentEntry		limitedMetadata			X
	# DocumentEntry		mimeType				R
	# DocumentEntry		objectType				R
	# DocumentEntry		patientId				R
	# DocumentEntry		practiceSettingCode		R
	# DocumentEntry		referenceIdList			O
	# DocumentEntry		repositoryUniqueId		O
	# DocumentEntry		serviceStartTime		R2
	# DocumentEntry		serviceStopTime			R2
	# DocumentEntry		size					O
	# DocumentEntry		sourcePatientId			R
	# DocumentEntry		sourcePatientInfo		O
	# DocumentEntry		title					O
	# DocumentEntry		typeCode				R
	# DocumentEntry		uniqueId				R
	# DocumentEntry		URI						O

	# SubmissionSet		author					R2
	# SubmissionSet		availabilityStatus		O
	# SubmissionSet		comments				O
	# SubmissionSet		contentTypeCode			R
	# SubmissionSet		entryUUID				R
	# SubmissionSet		homeCommunityId			O
	# SubmissionSet		intendedRecipient		O
	# SubmissionSet		limitedMetadata			X
	# SubmissionSet		patientId				R
	# SubmissionSet		sourceId				R
	# SubmissionSet		submissionTime			R
	# SubmissionSet		title					O
	# SubmissionSet		uniqueId				R

	# Folder is not implemented
	# Folder			availabilityStatus		O
	# Folder			codeList				R
	# Folder			comments				O
	# Folder			entryUUID				R
	# Folder			homeCommunityId			O
	# Folder			lastUpdateTime			O
	# Folder			limitedMetadata			X
	# Folder			patientId				R
	# Folder			title					R
	# Folder			uniqueId				R


	# In order to create coded attributes in the function below:
	# 1. Code Value – contains the assigned value of the code.
	# 2. Code Display Name - The display name used to represent the code (code values are not
	# necessarily human-friendly). Must be non-zero length.
	# 3. Coding Scheme - An identifier of the coding scheme that the code comes from.
	# For common Coding Schemes, see DICOM PS3.16, Table 8-1 Coding Schemes
	# (http://dicom.nema.org/medical/dicom/current/output/chtml/part16/chapter_8.html).
	# • If the Code Value is from a Coding Scheme in this table, the value for Coding
	# Scheme should be taken from either the “Coding Scheme UID” or the “Coding
	# Scheme Designator” column. If both are available, the value of Coding Scheme UID
	# should be used.
	# • If the Code Value is from a Coding Scheme that is not in this table, and if the Coding
	# Scheme can be identified with an OID, then the OID should be used.
	#
	# Taking information from HL7 message:
	#
	# Use the value hl7message['MSH.F10'] for instances
	# if you want to use the field MSH-10 into a variable that represents
	# some CDA metadata.
	#
	# format hl7message[SEGMENT.Fx.Ry.Cw.Sz] 	for single values
	#
	# If you want a string with multiple fiels, use:
	# hl7message.unescape(str(hl7message.segment('PID')[3][1])))
	# In both cases, the unescaped version of the string will be used.
	# Otherwise fill with fixed strings, or some python function.
	def fill_xds_metadata(self, hl7message):
		# The humans and/or machines that authored the document. This attribute contains the sub-
		# attributes: authorInstitution, authorPerson, authorRole, authorSpecialty and
		# authorTelecommunication. See ITI TF-3:4.2.3.1.4 Creating Author Attributes
		# authorPerson – zero or one
		# authorInstitution – zero or more
		# authorRole – zero or more
		# authorSpecialty – zero or more
		# authorTelecommunication – zero or more
		#
		# Required if known
		#
		# There may be multiple authors
		# There may be multiple authorvalue
		# authorrole can be one of authorInstitution, authorPerson, authorRole,
		#     authorSpecialty or authorTelecommunication
		# Implemented as an array of authors that contain a dictionary, which can have
		# multiple values for the authorvalue as array
		# one complete example of the whole structure might be:
		# self.m_DocumentEntry_author = [[
		# 	{
		# 		"authorvalue": ["^Smitty^Gerald^^^"],
		# 		"authorrole": "authorPerson",
		# 	},
		# 	{
		# 		"authorvalue": ["Cleveland Clinic", "Berea Community"],
		# 		"authorrole": "authorInstitution",
		# 	},
		# 	{
		# 		"authorvalue": ["Attending"],
		# 		"authorrole": "authorRole",
		# 	},
		# 	{
		# 		"authorvalue": ["Orthopedic"],
		# 		"authorrole": "authorSpecialty",
		# 	}
		# ], [
		# 	{
		# 		"authorvalue": ["^Dopplemeyer^Sherry^^^"],
		# 		"authorrole": "authorPerson",
		# 	},
		# 	{
		# 		"authorvalue": ["Cleveland Clinic", "Parma Community"],
		# 		"authorrole": "authorInstitution",
		# 	},
		# 	{
		# 		"authorvalue": ["Primary Surgeon"],
		# 		"authorrole": "authorRole",
		# 	},
		# 	{
		# 		"authorvalue": ["Orthopedic"],
		# 		"authorrole": "authorSpecialty",
		# 	}
		# ]]
		self.m_DocumentEntry_author = [[
			{
				"authorvalue": [hl7message['OBR.F32.R1.C1.S2']],
				"authorrole": "authorPerson",
			},
			{
				"authorvalue": ["Example hospital - Radiology department"],
				"authorrole": "authorInstitution"
			}
		]]


		# Represents the status of the DocumentEntry. A DocumentEntry shall have one of two availability
		# statuses:
		#	Approved The document is available for patient care.
		#	Deprecated The document is obsolete.
		#
		# Optional
		# 
		self.m_DocumentEntry_availabilityStatus = ""
		# self.m_DocumentEntry_availabilityStatus = "urn:oasis:names:tc:ebxml-regrep:StatusType:Approved"
		# self.m_DocumentEntry_availabilityStatus = "urn:oasis:names:tc:ebxml-regrep:StatusType:Deprecated"


		# The code specifying the high-level use classification of the document type (e.g., Report,
		# Summary, Images, Treatment Plan, Patient Preferences, Workflow). The typeCode specifies the
		# precise type of document from the user perspective. Valid values for classCode attribute are
		# specified by the policies of the creating entity. It is recommended that the creating entity draws
		# these values from a coding scheme providing a coarse level of granularity (about 10 to 100
		# entries). For example, XDS specifies that the XDS Affinity Domain will establish this list.
		# There shall be exactly zero or one ebRIM Classification containing a classCode for any
		# DocumentEntry
		#
		# Required
		#
		self.m_DocumentEntry_classCode = {
			"codeValue": "REPORTS",
			"codeDisplayName": "Imaging report",
			"codingScheme": "1.3.6.1.4.1.19376.1.2.6.1"
		}


		# Contains comments associated with the document.
		#
		# Optional
		#
		self.m_DocumentEntry_comments = ""
		# self.m_DocumentEntry_comments = "comment associated with the Document"


		# The code specifying the security and privacy tags of the document. These codes are set by policy
		# of the participants in the exchange, e.g., XDS affinity domain. confidentialityCode is part of a
		# codification scheme.
		# [1...1] Confidentiality Security Classification Label Field
		# [0...*] Sensitivity Security Category Label Field
		# [0...*] Compartment Security Category Label Field
		# [0...*] Integrity Security Category Label Field
		# [0...*] Handling Caveat Security Category Field
		#
		# Required
		#
		self.m_DocumentEntry_confidentialityCode = {
			"codeValue": "N",
			"codeDisplayName": "Normal Clinical Data",
			"codingScheme": "2.16.840.1.113883.5.25"
		}


		# Represents the time the author created the document
		#
		# Required
		#
		# import datetime
		# current_date = datetime.datetime.utcnow()
		# self.m_DocumentEntry_creationTime =  current_date.strftime("%Y%m%d%H%M%S")
		# self.m_DocumentEntry_creationTime = "20051224"
		self.m_DocumentEntry_creationTime = hl7message['OBR.F22']


		# The entryUUID attribute is a globally unique identifier primarily intended for internal document
		# management purposes. In contrast, the uniqueId attribute is used for external references (e.g.,
		# links, etc.).
		#
		# Required
		#
		self.m_DocumentEntry_entryUUID = "Document01"
		# self.m_DocumentEntry_entryUUID = "urn:uuid:{}".format(uuid.uuid1())


		# This list of codes represents the main clinical acts, such as a colonoscopy or an appendectomy,
		# being documented. In some cases, the event is inherent in the typeCode, such as a "History and
		# Physical Report" in which the procedure being documented is necessarily a "History and
		# Physical" act. An event can further specialize the act inherent in the typeCode, such as where it is
		# simply "Procedure Report" and the procedure was a "colonoscopy". When defining the value sets
		# for eventCodes, they should not conflict with the values inherent in the classCode,
		# practiceSettingCode or typeCode as such a conflict would create an ambiguous situation.
		#
		# Optional
		#
		self.m_DocumentEntry_eventCodeList = ""
		# self.m_DocumentEntry_eventCodeList = {
		#	"codeValue": "ExampleeventCode",
		#	"codeDisplayName": "eventCodeDisplayName",
		#	"codingScheme": "Example Event Code Scheme"
		# }


		# The code specifying the detailed technical format of the document. Along with the typeCode, it
		# should provide sufficient information to allow potential consumer to know if it will be able to
		# process the document.
		# The mimeType indicates the base format; the formatCode indicates the detailed-level technical
		# structure. Together with the mimeType, the formatCode used shall be sufficiently specific to
		# ensure processing/display by identifying a document encoding, structure and template (e.g., for a
		# CDA Document, the fact that it complies with a CDA schema, possibly a template and the choice
		# of a content-specific style sheet). The formatCode alone is often sufficiently specific, but an
		# actor that consumes metadata should not assume that it is.
		# The formatCode is often an indicator of the IHE Document Content Profile to which the
		# document conforms.
		# The mimeTypeSufficient formatCode of EV("urn:ihe:iti:xds:2017:mimeTypeSufficient",
		# "1.3.6.1.4.1.19376.1.2.3") may be used when the mimeType is sufficient to identify the technical
		# format of the document.
		# Format codes may be specified by multiple organizations. Format codes for Document Content
		# Profiles defined by the ITI domain shall be in URN format and have names with the prefix
		# urn:ihe:iti:
		# Format codes defined by other IHE domains shall have names with the prefix
		# urn:ihe:’domain initials’:
		# The IHE-managed codes and value set for formatCode are published on
		# http://wiki.ihe.net/index.php/IHE_Format_Codes.
		# Format codes defined by non-IHE domains should be a valid unique URN.
		#
		# Required
		#
		self.m_DocumentEntry_formatCode = {
			"codeValue": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
			"codeDisplayName": "mimeType Sufficient",
			"codingScheme": "1.3.6.1.4.1.19376.1.2.3"
		}


		# The hash of the contents of the document.
		# The hash attribute can be used to identify accidental document corruption, mistaken duplicate
		# IDs, etc. The SHA1 algorithm and hash attribute should not be used for identifying malicious
		# alterations.
		#
		# Optional
		#
		# Does not require a value here as it is received as argument
		# self.m_DocumentEntry_hash


		# This code represents the type of organizational setting of the clinical encounter during which the
		# documented act occurred.
		# In some cases, the setting of the encounter is inherent in the typeCode, such as "Diabetes Clinic
		# Progress Note". healthcareFacilityTypeCode shall be equivalent to or further specialize the value
		# inherent in the typeCode; for example, where the typeCode is simply "Clinic Progress Note" and
		# the value of healthcareFacilityTypeCode is "private clinic".
		#
		# Required
		#
		# self.m_DocumentEntry_healthcareFacilityTypeCode = {
		#	"codeValue": "HOSP",
		#	"codeDisplayName": "Hospital",
		#	"codingScheme": "2.16.840.1.113883.4.642.2.246"
		# }
		self.m_DocumentEntry_healthcareFacilityTypeCode = {
			"codeValue": "22232009",
			"codeDisplayName": "Hospital",
			"codingScheme": "2.16.840.1.113883.6.96"
		}


		# A globally unique identifier for a community where the DocumentEntry and document can be
		# accessed.
		#
		# Optional
		#
		self.m_DocumentEntry_homeCommunityId = ""
		# self.m_DocumentEntry_homeCommunityId = "urn:oid:1.2.3"


		# Specifies the human language of character data in the document
		#
		# Required
		#
		self.m_DocumentEntry_languageCode = "en-US"


		# Represents a participant within an authorInstitution who has legally authenticated or attested the
		# document. Legal authentication implies that a document has been signed manually or
		# electronically by the legalAuthenticator.
		# XCN format
		#
		# Optional
		#
		# legalAuthenticator shall be in XCN format
		self.m_DocumentEntry_legalAuthenticator = ""
		# self.m_DocumentEntry_legalAuthenticator = "^Welby^Marcus^^^Dr^MD"


		# Indicates whether the Document Entry was created using the less rigorous requirements of
		# metadata as defined for the Metadata-Limited Document Source Actor.
		#
		# Forbidden
		#
		# global self.m_DocumentEntry_limitedMetadata
		# self.m_DocumentEntry_limitedMetadata = Forbidden


		# MIME type of the document in the Repository
		#
		# Required
		#
		self.m_DocumentEntry_mimeType = "text/xml"


		# The objectType attribute reflects the type of DocumentEntry. As described in Section 4.1.1, there
		# are two DocumentEntry types: Stable Document Entry and On-Demand Document Entry. A
		# Stable Document Entry contains metadata about an already created document available for
		# retrieval is a Document Entry and is designated by setting objectType equal to the UUID for
		# Stable (see Section 4.2.5.2 for the UUID). An On-Demand Document Entry contains metadata
		# which can be used to create an on-demand document which collects the latest, most recent
		# available information at the time of retrieval. It is designed by setting an objectType equal to the
		# UUID for on-demand (see Section 4.2.5.2 for the UUID).
		# The value of the objectType is coded in the objectType XML attribute on the ExtrinsicObject
		# representing the DocumentEntry. In the example below, the objectType is urn:uuid:7edca82f-
		# 054d-47f2-a032-9b2a5b5186c1 and reflects a stable DocumentEntry.
		#
		# Required
		#
		# Stable Document Entry
		self.m_DocumentEntry_objectType = "urn:uuid:7edca82f-054d-47f2-a032-9b2a5b5186c1"
		# On-Demand Document Entry
		# self.m_DocumentEntry_objectType = "urn:uuid:34268e47-fdf5-41a6-ba33-82133c465248"


		# This call finds the PID-3 repetition that has the patient ID in the 
		# XDS affinity domain
		# Use this variable instead of "repetition" in the HL7 message
		xad_pid_repetition = hl7_v2x_receiver.Hl7v2x.hl7_find_xad_pid_repetition(hl7message)


		# The patientId represents the subject of care of the document. For XDS the patient identifier
		# domain is the XDS Affinity Domain Patient Identifier Domain (XAD-PID).
		# Within a submission request, the value of patientId of the DocumentEntries shall match that of
		# the SubmissionSet
		# The format of the patientId value is CX; see Table 4.2.3.1.7-2.
		# It shall contain two parts:
		# • Assigning Authority Domain Id (organization that issued the Id)
		# • An Id from the above Assigning Authority.
		# No other values are allowed, as specified for the CX type. Using HL7 terminology, no other
		# values are allowed in the components of the coded value, nor are further subcomponents
		# allowed.
		#
		# Required
		#
		# Patient ID in CX format
		# self.m_DocumentEntry_patientId = "6578946^^^&1.3.6.1.4.1.21367.2005.3.7&ISO"
		self.m_DocumentEntry_patientId = hl7message.unescape(
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(1)) +
			"^^^&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(2)) +
			"&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(3))
		)


		# The code specifying the clinical specialty where the act that resulted in the document was
		# performed (e.g., Family Practice, Laboratory, Radiology). It is suggested that the creating entity
		# draws these values from a coding scheme providing a coarse level of granularity (about 10 to 100
		# entries).
		#
		# Required
		#
		# This attribute shall be populated by the Imaging Document Source to
		# describe the high-level imaging specialty such as (R-3027B, SRT,
		# “Radiology”), (R-3026B, SRT, “Pathology”), or (R-30248, SRT,
		# “Cardiology”). The list of acceptable values is constrained by the
		# organization managing the XDS Registry (i.e., the XDS Affinity
			# Domain).
		# It is strongly recommended to use the values from the DICOM Content
		# Mapping Resource (PS3.16) Context Group CID 7030.
		# http://dicom.nema.org/medical/dicom/current/output/html/part16.html#sect_CID_7030
		# self.m_DocumentEntry_practiceSettingCode = {
		#	"codeValue": "441662001",
		#	"codeDisplayName": "Diagnostic Imaging",
		#	"codingScheme": "2.16.840.1.113883.6.96"
		# }
		self.m_DocumentEntry_practiceSettingCode = {
			"codeValue": "R-3027B",
			"codeDisplayName": "Radiology",
			"codingScheme": "2.16.840.1.113883.6.96"
		}


		# These Identifiers may be internal or external identifiers, e.g., Identifiers may be Accession
		# Numbers, Order Numbers, Referral Request Identifiers, XDW Workflow Instance Identifiers,
		# etc. The referenceIdList contains Identifiers CXi encoded, as specified in Table 4.2.3.1.7-2.
		# Max length is 256 characters.
		# Coded as an ebRIM Slot. May have multiple values.
		#
		# Optional
		#
		# self.m_DocumentEntry_referenceIdList = ""
		# A simple array of external identifiers
		self.m_DocumentEntry_referenceIdList = [
			hl7message['OBR.F18'] + "^^^^urn:ihe:iti:xds:2013:accession"
		]
		# self.m_DocumentEntry_referenceIdList = [ "1.2.3.12.78.23^^^&1.2.3.4&ISO^urn:ihe:iti:xds:2013:uniqueId" ]
		# TODO: Why sectra uses also urn:sectra:iti:xds:2015:referenceAndStudyIdList


		# The globally unique, immutable, identifier of the repository where the document referenced by
		# the Document Entry can be accessed. This unique identifier for the repository may be used to
		# identify and connect to the specific repository to access the document
		#
		# Optional
		#
		# Identifier of the repository where the document referenced by
		# the Document Entry can be accessed.
		self.m_DocumentEntry_repositoryUniqueId = ""
		# self.m_DocumentEntry_repositoryUniqueId = "1.3.6.1.4.5"


		# Represents the start time of the service being documented (clinically significant, but not
		# necessarily when the document was produced or approved). This may be the same as the
		# encounter time in case the service was delivered during an encounter. Encounter time is not
		# coded in metadata but may be coded within the document.
		# Note: If needed, other times associated with the document, such as time of approval, are to be
		# recorded within the document.
		# The format of serviceStartTime value is DTM
		#
		# Required if known
		#
		# The format of the serviceStartTime value is DTM
		# self.m_DocumentEntry_serviceStartTime = "200412230800"
		self.m_DocumentEntry_serviceStartTime = hl7message['OBR.F22']


		# Represents the stop time of the service being documented (clinically significant, but not
		# necessarily when the document was produced or approved). This may be the same as the
		# encounter time in case the service was delivered during an encounter. Encounter time is not
		# coded in metadata but may be coded within the document.
		# If the service happens at a point in time, this attribute shall contain the same value as the
		# serviceStartTime.
		# The format of serviceStopTime value is DTM
		#
		# Required if known
		#
		# The format of the serviceStopTime value is DTM
		# self.m_DocumentEntry_serviceStopTime = "200412230801"
		self.m_DocumentEntry_serviceStopTime = hl7message['OBR.F22']


		# Size in bytes of the byte stream that comprises the document
		#
		# Optional
		#
		# Does not require a value for self.m_DocumentEntry_size as it is received as argument
		# self.m_DocumentEntry_size


		# The sourcePatientId represents the subject of care’s medical record identifier (e.g., Patient Id) in
		# the local patient identifier domain of the creating entity.
		# Coded as an ebRIM Slot with the value encoded according the CX
		# datatype (see Table 4.2.3.1.7-2)
		#
		# Required
		#
		# self.m_DocumentEntry_sourcePatientId = "j98789^^^&1.2.3.4.343.1&ISO"
		self.m_DocumentEntry_sourcePatientId = hl7message.unescape(
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(1)) +
			"^^^&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(2)) +
			"&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(3))
		)


		# This attribute contains demographics information at the time of submission of the patient to
		# whose medical record this document belongs.
		# This information typically includes: the patient first and last name, sex, and birth date. Policies at
		# the creating entity may require more or less specific information and format.
		# This patient information is not intended to be updated once the document is registered (just as the
		# document content and metadata itself will not be updated without replacing the previous
		# document). As sourcePatientInfo may have been updated by the source actor, it may no longer be
		# in use within the Document Source (EHR-CR). It is only intended as an audit/checking
		# mechanism and has occasional use for Document Consumer Actors.
		# Coding:
		# Coded as an ebRIM Slot. If present, each rim:Value contains a Field (see Table 4.2.3.1.7-2 for a
		# description of the Field datatype). Multiple rim:Value elements may exist for the same field
		# name as a way to implement repetition; there shall be at most one rim:Value element for each of
		# the PID-7 and PID-8 fields. Only field defined for the PID segment shall be used.
		# Maximum length of each rim:Value is 256 characters. The sourcePatientInfo attribute should
		# include:
		# • PID-3 (source patient identifier list)
		# • PID-5 (source patient name)
		# • If multiple patient names are present, then PID-5.7 “Name Type Code” and PID-5.8
		#   “Name Representation Code” should be valued in each entry.
		# • PID-7 (source patient date of birth)
		# • PID-8 (source patient gender)
		# The sourcePatientInfo attribute should not include values for PID-2 (patient id), PID-4 (alternate
		# patient id), PID-12 (country code), or PID-19 (social security number).
		#
		# Optional
		#
		# sourcePatientInfo should be an array of values, 
		# PID-3 (source patient identifier list)
		# PID-5 (source patient name)
		# If multiple patient names are present, then PID-5.7 “Name Type Code” and PID-5.8
		#     “Name Representation Code” should be valued in each entry.
		# PID-7 (source patient date of birth)
		# PID-8 (source patient gender)
		# self.m_DocumentEntry_sourcePatientInfo = ""
		# self.m_DocumentEntry_sourcePatientInfo = [
		# 	"PID-3|D\E\ID1-1^^^&1.3.6&ISO~ID2^^^&1.3.11&ISO",
		# 	"PID-3|YZP-2^^^&1.3.42&ISO~ABC-3^^^&1.3.3.14&ISO",
		# 	"PID-5|DICTAPHONE^ONE^^^",
		# 	"PID-7|19650120",
		# 	"PID-8|M",
		# 	"PID-11|100 Main St^^BURLINGTON^MA^01803^USA"
		# ]
		# Adds all patient domain ids into a list
		# TODO: Sending many PID-3 is currently not working for XDS toolkit
		# TODO: But i think it would be acceptable from the description above
		self.m_DocumentEntry_sourcePatientInfo = []
		for domain_id in range(1, len(hl7message.segment('PID')(3)) + 1):
			self.m_DocumentEntry_sourcePatientInfo.append("PID-3|" +
				hl7message.unescape(
					str(hl7message.segment('PID')(3)(domain_id)(1)) +
					"^^^&" +
					str(hl7message.segment('PID')(3)(domain_id)(4)(2)) +
					"&" +
					str(hl7message.segment('PID')(3)(domain_id)(4)(3))
				)
			)
		# Adds remaining sourcePatientInfo
		self.m_DocumentEntry_sourcePatientInfo.append("PID-5|" + hl7message.unescape(str(hl7message.segment('PID')(5))))
		self.m_DocumentEntry_sourcePatientInfo.append("PID-7|" + hl7message['PID.F7'])
		self.m_DocumentEntry_sourcePatientInfo.append("PID-8|" + hl7message['PID.F8'])


		# Represents the title of the document.
		# Clinical documents often do not have a title; in such case the classCode (e.g., a "consultation" or
		# "progress note") is often used as the title. In that case, the title is usually omitted.
		#
		# Optional
		#
		# self.m_DocumentEntry_title = "Example Document Title"
		self.m_DocumentEntry_title = ""


		# The code specifying the precise type of document from the user’s perspective. It is recommended
		# that the creating entity draw these values from a coding scheme providing a fine level of
		# granularity such as LOINC.
		#
		# Required
		#
		# The exam code
		self.m_DocumentEntry_typeCode = {
			"codeValue": "18748-4",
			"codeDisplayName": "Diagnostic Imaging Study",
			"codingScheme": "2.16.840.1.113883.6.1"
		}


		# Globally unique identifier assigned to the document by its creator
		# See section 4.2.3.2.26 DocumentEntry.uniqueId in ITI TF-3
		#
		# Required
		#
		# https://wiki.ihe.net/index.php/Creating_Unique_IDs_-_OID_and_UUID
		# an OID from an UUID must start with "2.25." and followed by the straight decimal encoding of the UUID as an integer
		self.m_DocumentEntry_uniqueId = {
			"value": "2.25.{}".format(uuid.uuid1().int),
			"codeDisplayName": "XDSDocumentEntry.uniqueId",
		}


		# The URI attribute contains the URI for the document.
		# Max length is 256 characters. Coded as an ebRIM Slot. Shall have only a single value.
		#
		# Optional
		#
		self.m_DocumentEntry_URI = ""
		# self.m_DocumentEntry_URI = "DOC001.XML"


		###############################################################################


		# Represents the humans and/or machines that authored the SubmissionSet. See Section 4.2.3.1.4
		# for details on creating the structure.
		# authorPerson – zero or one
		# authorInstitution – zero or more
		# authorRole – zero or more
		# authorSpecialty – zero or more
		# authorTelecommunication – zero or more
		#
		# Required if known
		#
		# There may be multiple authors
		# There may be multiple authorvalue
		# authorrole can be one of authorInstitution, authorPerson, authorRole,
		#     authorSpecialty or authorTelecommunication
		# Implemented as an array of authors that contain a dictionary, which can have
		# multiple values for the authorvalue as array
		# self.m_SubmissionSet_author = [[
		# 	{
		# 		"authorvalue": ["^Dopplemeyer^Sherry^^^"],
		# 		"authorrole": "authorPerson",
		# 	},
		# 	{
		# 		"authorvalue": ["Cleveland Clinic", "Berea Community"],
		# 		"authorrole": "authorInstitution",
		# 	},
		# 	{
		# 		"authorvalue": ["Primary Surgeon"],
		# 		"authorrole": "authorRole",
		# 	},
		# 	{
		# 		"authorvalue": ["Orthopedic"],
		# 		"authorrole": "authorSpecialty",
		# 	}
		# ]]
		self.m_SubmissionSet_author = [[
			{
				"authorvalue": [hl7message['OBR.F32.R1.C1.S2']],
				"authorrole": "authorPerson",
			},
			{
				"authorvalue": ["Example hospital - Radiology department"],
				"authorrole": "authorInstitution"
			}
		]]


		# Represents the status of the SubmissionSet. Since the deprecation of SubmissionSets is not
		# allowed, this value shall always be Approved.
		#
		# Optional
		#
		# Does not need to be implemented
		# Since the deprecation of SubmissionSets is not allowed, this value shall always be Approved.
		# self.m_SubmissionSet_availabilityStatus


		# Contains comments associated with the SubmissionSet
		#
		# Optional
		#
		# self.m_SubmissionSet_comments = "Annual physical"
		self.m_SubmissionSet_comments = ""


		# The code specifying the type of clinical activity that resulted in placing these DocumentEntries,
		# Folders, and/or Associations in this SubmissionSet. These values are to be drawn from a
		# vocabulary defined by the creating entity that contributed the SubmissionSet.
		#
		# Required
		#
		self.m_SubmissionSet_contentTypeCode = {
			"codeValue": hl7message['OBR.F4.R1.C1'],
			"codeDisplayName": hl7message['OBR.F4.R1.C2'],
			"codingScheme": hl7message['OBR.F4.R1.C3']
		}


		# The entryUUID attribute is a globally unique identifier primarily intended for internal document
		# management purposes. In contrast, the uniqueId attribute is used for external references (e.g.,
		# links, etc.).
		#
		# Required
		#
		# self.m_SubmissionSet_entryUUID = "urn:uuid:{}".format(uuid.uuid1())
		self.m_SubmissionSet_entryUUID = "SubmissionSet01"


		# A globally unique identifier for a community.
		#
		# Optional
		#
		self.m_SubmissionSet_homeCommunityId = ""
		# self.m_SubmissionSet_homeCommunityId = "urn:oid:1.2.3"


		# Represents the organization(s) or person(s) for whom the SubmissionSet is intended at time of
		# submission. Each slot value shall include at least one of the organization, person, or
		# telecommunications address fields described below. It is highly recommended to define the
		# organization for all the persons, avoiding errors in the transmission of the documents
		# The value is coded as zero or more values within a single ebRIM Slot in the SubmissionSet.
		#
		# Optional
		#
		self.m_SubmissionSet_intendedRecipient = ""
		# self.m_SubmissionSet_intendedRecipient = [
		#	"Some Hospital^^^^^^^^^1.2.3.9.1789.45|^Wel^Marcus^^^Dr^MD|^^Internet^mwel@healthcare.example.org",
		#	"Some Hospital^^^^^^^^^1.2.3.9.1789.45|^Peirre^LaPointe^^^Dr^MD",
		#	"|12345^LaShawn^James^^Dr^MD",
		#	"MainHospital^^^^^^^^^1.2.3.4.5.6.7.8.9.1789.2364",
		#	"^^Internet^dr.oz@healthcare.example.org"
		# ]


		# Indicates whether the SubmissionSet was created using the less rigorous requirements of
		# metadata as defined for the Metadata-Limited Document Source
		#
		# Forbidden
		#
		# self.m_SubmissionSet_limitedMetadata = Forbidden


		# The patientId represents the primary subject of care of the SubmissionSet
		# The format of the patientId value is CX (see Table 4.2.3.1.7-2)
		# It shall contain two parts:
		#    Assigning Authority Domain Id (organization that issued the Id).
		#    An Id from the above Assigning Authority.
		# No other values are allowed, as specified for the CX type. Using HL7 terminology, no other
		# values are allowed in the components of the coded value, nor are further subcomponents
		# allowed.
		#
		# Required
		#
		# self.m_SubmissionSet_patientId = "6578946^^^&1.3.6.1.4.1.21367.2005.3.7&ISO"
		self.m_SubmissionSet_patientId = hl7message.unescape(
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(1)) +
			"^^^&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(2)) +
			"&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(3))
		)


		# The globally unique, immutable, identifier of the entity that contributed the SubmissionSet.
		# When a "broker" is involved in sending SubmissionSets from a collection of client systems, it
		# shall use a different sourceId for submissions from each separate system to allow for tracking.
		#
		# Required
		#
		self.m_SubmissionSet_sourceId = "1.3.6.1.4.1.55196.1.1.2.5"


		# Represents the point in time at the creating entity when the SubmissionSet was created
		# This shall be provided by the submitting system
		#
		# Required
		#
		# self.m_SubmissionSet_submissionTime should be filled with the time of submission
		# self.m_SubmissionSet_submissionTime = "20041225235050"
		import datetime
		current_date = datetime.datetime.utcnow()
		self.m_SubmissionSet_submissionTime =  current_date.strftime("%Y%m%d%H%M%S")


		# Shall contain the title of the SubmissionSet
		#
		# Optional
		#
		# self.m_SubmissionSet_title = "Example Submission Set Title"
		self.m_SubmissionSet_title = ""


		# The globally unique identifier for the SubmissionSet assigned by the entity that contributed the
		# SubmissionSet
		#
		# Required
		#
		# https://wiki.ihe.net/index.php/Creating_Unique_IDs_-_OID_and_UUID
		# an OID from an UUID must start with "2.25." and followed by the straight decimal encoding of the UUID as an integer
		self.m_SubmissionSet_uniqueId = "2.25.{}".format(uuid.uuid1().int)


		###############################################################################


		# Folder variables are not implemented


###################################################################
## End of Main configuration
###################################################################


	#
	## Process an xml response from a file
	# TODO: Function for debug purposes, not fully implemented
	#
	def read_from_file(self, xds_request_file):
		if not os.path.isfile(xds_request_file) :
			raise RuntimeError('XDS template file not found (%s). Exiting.', xds_request_file)

		tree = etree.parse(xds_request_file)
		return etree.XMLParser()


	#
	## convert2xds takes an HL7 message and converts to an [ITI-41] transaction
	#
	def convert_to_ITI41(self, hl7message):
		logger.info('Building XDS [ITI-41] transaction')
		# An HL7 v2.x message was received, and is now going to be converted
		# into a CDA and sent as an IHE XDS.b document source to a document
		# repository  [ITI-41] (Provide&RegisterDocumentSet - b)

		# Generate an HTTP multipart Content-ID for the XDS request
		xdsrequest_id = "0.urn:uuid:{}@oru2xds".format(str(uuid.uuid1()))
		# Generate an HTTP multipart Content-ID for the CDA
		cda_id = "1.urn:uuid:{}@oru2xds".format(str(uuid.uuid1()))

		MyCDA = HL7CdaBuilder()
		# Build CDA using HL7 message fields
		cda_str = MyCDA.build_cda(hl7message, cda_id)
		# cda_str is a string, not lxml
		# Calculate size in bytes of CDA
		cda_size = MyCDA.calculate_cda_size(cda_str)
		# Calculate SHA-1 hash of CDA
		cda_hash = MyCDA.calculate_cda_hash(cda_str)

		# Provide and Register Document Set-b transaction [ITI-41]
		# Builds metadata using HL7 message fields and independent data
		xds_request_tree = self.build_ProvideAndRegisterDocumentSetRequest(hl7message, xdsrequest_id, cda_id, cda_hash, cda_size)
		# xds_request_tree is lxml

		# Build SOAP envelope using CDA and XDS ProvideAndRegisterDocumentSetRequest
		soap = SOAP(xds_request_tree)
		# Send SOAP using MTOM/XOP
		xds_response_xml = soap.send_http_multipart(cda_id, cda_str)

		# Process IHE XDS [ITI-41] response
		response = self.process_xds_response(soap.uuid, xds_response_xml)
		# XDS response might be "Success", "Failure", "PartialFailure"
		logger.info("Overall XDS Provide and Register Document Set-b Response is: %s", response)
		logger.info('XDS transaction finished')

		# If everything went OK with the SOAP transaction, but the  Provide and Register Document Set-b Response ends-up in some failure, then we raise an error anyways
		if response != "Success":
			raise RuntimeError(response)


	###################################################################
	## Example IHE XDS responses
	###################################################################
	# A response to a query request that indicates success with no warnings and no documents found is:
	#xml = '''
	#<query:AdhocQueryResponse
	#status = "urn:oasis:names:tc:ebxml-regrep:ResponseStatusType:Success">
	#<rim:RegistryObjectList/>
	#</query:AdhocQueryResponse >
	#'''
	#
	# An example response to a Submission Request that reports two errors and one warning
	#xml = '''
	#<rs:RegistryResponse xmlns:rs = "urn:oasis:names:tc:ebxml-regrep:xsd:rs:3.0"
	#status = "urn:oasis:names:tc:ebxml-regrep:ResponseStatusType:Failure">
	#<rs:RegistryErrorList
	#highestSeverity = "urn:oasis:names:tc:ebxml-regrep:ErrorSeverityType:Error">
	#	<rs:RegistryError
	#	errorCode = "XDSPatientIdDoesNotMatch"
	#	codeContext = "Patient Id in Document (Document1) does not match SubmissionSet"
	#	location = ""
	#	severity = "urn:oasis:names:tc:ebxml-regrep:ErrorSeverityType:Error"/>
	#	<rs:RegistryError
	#	errorCode = "XDSRegistryMetadataError"
	#	codeContext = "RegistryPackage (SubmissionSet) is not labeled as SubmissionSet or Folder"
	#	location = ""
	#	severity = "urn:oasis:names:tc:ebxml-regrep:ErrorSeverityType:Error"/>
	#	<rs:RegistryError
	#	errorCode = "XDSExtraMetadataNotSaved"
	#	codeContext = "Extra Metadata – localinfo – not saved"
	#	location = ""
	#	severity = "urn:oasis:names:tc:ebxml-regrep:ErrorSeverityType:Warning"/>
	#</rs:RegistryErrorList>
	#</rs:RegistryResponse>
	#'''
	#
	## Process XDS response in an XML tree
	#
	def process_xds_response(self, content_id1, response_tree):
		# Must be a valid XDS response urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-bResponse
		# print(type(response_tree.xpath("//wsa:Action", namespaces = NSMAP)))
		if response_tree.find('.//soapenv:Header/wsa:Action', namespaces = NSMAP).text != 'urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-bResponse':
			raise RuntimeError("Does not seem to be a valid ProvideAndRegisterDocumentSet-bResponse")
		
		# TODO: Check that message response is related with our message sent
		if response_tree.find('.//soapenv:Header/wsa:RelatesTo', namespaces = NSMAP).text != content_id1:
			raise RuntimeError("The response does not seem to match our request ID")
		
		# Possible response values are:
		# urn:oasis:names:tc:ebxml-regrep:ResponseStatusType:Success
		# urn:oasis:names:tc:ebxml-regrep:ResponseStatusType:Failure
		# urn:ihe:iti:2007:ResponseStatusType:PartialSuccess
		rs_status = response_tree.find('.//soapenv:Body/rs:RegistryResponse', namespaces = NSMAP).attrib['status']

		if rs_status == 'urn:oasis:names:tc:ebxml-regrep:ResponseStatusType:Success':
			status = "Success"
		elif rs_status == 'urn:oasis:names:tc:ebxml-regrep:ResponseStatusType:Failure':
			status = "Failure"
		elif rs_status == 'urn:ihe:iti:2007:ResponseStatusType:PartialSuccess':
			status = "PartialSuccess"
		else:
			raise RuntimeError("Unknown value in urn:ihe:iti:2007:ResponseStatusType")
		logger.info("Server response status is: %s", status)

		# If everything is OK, stop here
		if status == "Success":
			return status

		# If there are errors
		# TODO: highestSeverity might not exist?
		# rel = response_tree.xpath("//rs:RegistryErrorList", namespaces = NSMAP)
		# assert len(rel) == 1
		# logger.debug("Highest severity: %s", rel[0].attrib["highestSeverity"].replace("urn:oasis:names:tc:ebxml-regrep:ErrorSeverityType:", ""))
		logger.info("RegistryErrorList size: %s", len(response_tree.findall('.//soapenv:Body/rs:RegistryResponse/rs:RegistryErrorList/rs:RegistryError', namespaces = NSMAP)))

		for RegError in response_tree.iterfind('.//soapenv:Body/rs:RegistryResponse/rs:RegistryErrorList/rs:RegistryError', namespaces = NSMAP):
			# print(etree.tostring(RegError, pretty_print = True))
			for element in RegError.iter():
				logger.debug("RegistryError:")
				logger.debug("    codeContext - %s", element.attrib["codeContext"])
				logger.debug("    errorCode - %s", element.attrib["errorCode"])
				logger.debug("    location - %s", element.attrib["location"])
				logger.debug("    severity - %s", element.attrib["severity"])

		return "XDS Provide and Register Document Set-b Response is a failure. Check oru2xds logs for more details."


	# Convert HL7 characters that are special characters in XML content
	# Not needed as lxml takes care of this
	# &lt; (<), &amp; (&), &gt; (>), &quot; ("), and &apos; (')
	# def escape_xml(self, field_value) :
	#	mappings = str.maketrans({
	#		"<":  r"&lt;",
	#		"&":  r"&amp;",
	#		">": r"&gt;",
	#		"\"":  r"&quot;",
	#		"'":  r"&apos;",
	#	})
	#	field_value = field_value.translate(mappings)
	#	return field_value


	#
	## Create the next symbolic ID that identifies objects in the submission
	#
	def get_next_symbolic_id(self) :
		self.object_symbolic_id += 1
		return "id_{}".format(self.object_symbolic_id)


	###################################################################
	## Document Entry
	###################################################################
	# DocumentEntry – metadata describing a Document

	# The humans and/or machines that authored the document. This attribute contains the sub-
	# attributes: authorInstitution, authorPerson, authorRole, authorSpecialty and
	# authorTelecommunication. See ITI TF-3:4.2.3.1.4 Creating Author Attributes
	# authorPerson – zero or one
	# authorInstitution – zero or more
	# authorRole – zero or more
	# authorSpecialty – zero or more
	# authorTelecommunication – zero or more
	# TODO: Check compliance with cardinality of each authorRole
	#
	# Required if known
	#
	def DocumentEntry_author(self, parentNode) :
		if len(self.m_DocumentEntry_author) == 0:
			logger.warning("Not creating DocumentEntry.author as values are empty")
			return

		# For each author
		for author in self.m_DocumentEntry_author:
			logger.debug("DocumentEntry author:")
			# Create a Classification
			classification = etree.Element(rim_prefix + "Classification",
				nsmap = nsmap_rim,
				classificationScheme = "urn:uuid:93606bcf-9494-43ec-9b4e-a7748d1a838d",
				classifiedObject = self.documentEntry_entryUUID(),
				nodeRepresentation = "",
				objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification",
				id = self.get_next_symbolic_id()
			)
			for authorrole in author:
				# There is an authorvalue, authorrole pair
				slot = etree.SubElement(classification, rim_prefix + "Slot")
				logger.debug("    authorrole: \"%s\"", authorrole["authorrole"])
				slot.attrib['name'] = authorrole["authorrole"]
				valuelist = etree.SubElement(slot, rim_prefix + "ValueList")
				# authorvalue is an array
				for authorvalue in authorrole["authorvalue"]:
					sub = etree.SubElement(valuelist, rim_prefix + "Value")
					logger.debug("    authorvalue: \"%s\"", authorvalue)
					sub.text = authorvalue
			# Add this author to the list of authors
			parentNode.append(classification)
		return


	# Represents the status of the DocumentEntry. A DocumentEntry shall have one of two availability
	# statuses:
	#	Approved The document is available for patient care.
	#	Deprecated The document is obsolete.
	#
	# Optional
	#
	def DocumentEntry_availabilityStatus(self, parentNode) :
		if not self.m_DocumentEntry_availabilityStatus:
			logger.warning("Not creating DocumentEntry.availabilityStatus as value is empty")
			return

		logger.debug("DocumentEntry availabilityStatus: \"%s\"", self.m_DocumentEntry_availabilityStatus)
		parentNode.attrib['status'] = self.m_DocumentEntry_availabilityStatus
		return

	# The code specifying the high-level use classification of the document type (e.g., Report,
	# Summary, Images, Treatment Plan, Patient Preferences, Workflow). The typeCode specifies the
	# precise type of document from the user perspective. Valid values for classCode attribute are
	# specified by the policies of the creating entity. It is recommended that the creating entity draws
	# these values from a coding scheme providing a coarse level of granularity (about 10 to 100
	# entries). For example, XDS specifies that the XDS Affinity Domain will establish this list.
	# There shall be exactly zero or one ebRIM Classification containing a classCode for any
	# DocumentEntry
	#
	# Required
	#
	def DocumentEntry_classCode(self, parentNode) :
		if not self.m_DocumentEntry_classCode["codeValue"]:
			logger.error("Not creating DocumentEntry.classCode as value is empty")
			raise RuntimeError("DocumentEntry.classCode is a required field. Aborting XDS submission")

		logger.debug("DocumentEntry classCode:")
		logger.debug("    codeValue: \"%s\"", self.m_DocumentEntry_classCode["codeValue"])
		logger.debug("    codeDisplayName: \"%s\"", self.m_DocumentEntry_classCode["codeDisplayName"])
		logger.debug("    codingScheme: \"%s\"", self.m_DocumentEntry_classCode["codingScheme"])

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		classcode = E.Classification(
			E.Slot(
				E.ValueList(
					E.Value(self.m_DocumentEntry_classCode["codingScheme"])
				),
				name = "codingScheme"
			),
			E.Name(
				E.LocalizedString(
					value = self.m_DocumentEntry_classCode["codeDisplayName"]
				)
			),
			classificationScheme = "urn:uuid:41a5887f-8865-4c09-adf7-e362475b143a",
			classifiedObject = self.documentEntry_entryUUID(),
			nodeRepresentation = self.m_DocumentEntry_classCode["codeValue"],
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification",
			id = self.get_next_symbolic_id()
		)
		parentNode.append(classcode)
		return


	# Contains comments associated with the document.
	#
	# Optional
	#
	def DocumentEntry_comments(self, parentNode) :
		if not self.m_DocumentEntry_comments:
			logger.warning("Not creating DocumentEntry.comments as value is emtpy")
			return

		logger.debug("DocumentEntry comments: \"%s\"", self.m_DocumentEntry_comments)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		comments = E.Description(
			E.LocalizedString(
				value = self.m_DocumentEntry_comments
			)
		)
		parentNode.append(comments)
		return


	# The code specifying the security and privacy tags of the document. These codes are set by policy
	# of the participants in the exchange, e.g., XDS affinity domain. confidentialityCode is part of a
	# codification scheme.
	# [1...1] Confidentiality Security Classification Label Field
	# [0...*] Sensitivity Security Category Label Field
	# [0...*] Compartment Security Category Label Field
	# [0...*] Integrity Security Category Label Field
	# [0...*] Handling Caveat Security Category Field
	# TODO: Only one confidentiality code is currently supported
	#
	# Required
	#
	def DocumentEntry_confidentialityCode(self, parentNode):
		if not self.m_DocumentEntry_confidentialityCode["codeValue"]:
			logger.error("Not creating DocumentEntry.confidentialityCode as value is empty")
			raise RuntimeError("DocumentEntry.confidentialityCode is a required field. Aborting XDS submission")

		logger.debug("DocumentEntry confidentialityCode:")
		logger.debug("    codeValue: \"%s\"", self.m_DocumentEntry_confidentialityCode["codeValue"])
		logger.debug("    codeDisplayName: \"%s\"", self.m_DocumentEntry_confidentialityCode["codeDisplayName"])
		logger.debug("    codingScheme: \"%s\"", self.m_DocumentEntry_confidentialityCode["codingScheme"])

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		confidentialitycode = E.Classification(
			E.Slot(
				E.ValueList(
					E.Value(self.m_DocumentEntry_confidentialityCode["codingScheme"])
				),
				name = "codingScheme"
			),
			E.Name(
				E.LocalizedString(
					value = self.m_DocumentEntry_confidentialityCode["codeDisplayName"]
				)
			),
			classificationScheme = "urn:uuid:f4f85eac-e6cb-4883-b524-f2705394840f",
			classifiedObject = self.documentEntry_entryUUID(),
			nodeRepresentation = self.m_DocumentEntry_confidentialityCode["codeValue"],
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification",
			id = self.get_next_symbolic_id()
		)
		parentNode.append(confidentialitycode)
		return


	# Represents the time the author created the document
	# TODO: Check date is valid
	#
	# Required
	#
	def DocumentEntry_creationTime(self, parentNode) :
		if not self.m_DocumentEntry_creationTime:
			logger.error("Not creating DocumentEntry.creationTime as value is empty")
			raise RuntimeError("DocumentEntry.creationTime is a required field. Aborting XDS submission")

		logger.debug("DocumentEntry creationTime: \"%s\"", self.m_DocumentEntry_creationTime)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		creationtime = E.Slot(
			E.ValueList(
				E.Value(self.m_DocumentEntry_creationTime)
			),
			name = "creationTime"
		)
		parentNode.append(creationtime)
		return


	# The entryUUID attribute is a globally unique identifier primarily intended for internal document
	# management purposes. In contrast, the uniqueId attribute is used for external references (e.g.,
	# links, etc.).
	#
	# Required
	#
	def documentEntry_entryUUID(self) :
		if not self.m_DocumentEntry_entryUUID:
			logger.error("Not creating DocumentEntry.entryUUID as value is empty")
			raise RuntimeError("DocumentEntry.entryUUID is a required field. Aborting XDS submission")

		# logger.debug("DocumentEntry entryUUID: \"%s\"", self.m_DocumentEntry_entryUUID)
		return self.m_DocumentEntry_entryUUID


	# This list of codes represents the main clinical acts, such as a colonoscopy or an appendectomy,
	# being documented. In some cases, the event is inherent in the typeCode, such as a "History and
	# Physical Report" in which the procedure being documented is necessarily a "History and
	# Physical" act. An event can further specialize the act inherent in the typeCode, such as where it is
	# simply "Procedure Report" and the procedure was a "colonoscopy". When defining the value sets
	# for eventCodes, they should not conflict with the values inherent in the classCode,
	# practiceSettingCode or typeCode as such a conflict would create an ambiguous situation.
	#
	# Optional
	#
	def DocumentEntry_eventCodeList(self, parentNode) :
		if not self.m_DocumentEntry_eventCodeList["codeValue"]:
			logger.warning("Not creating DocumentEntry.eventCodeList as value is empty")
			return

		logger.debug("DocumentEntry eventCodeList:")
		logger.debug("    codeValue: \"%s\"", self.m_DocumentEntry_eventCodeList["codeValue"])
		logger.debug("    codeDisplayName: \"%s\"", self.m_DocumentEntry_eventCodeList["codeDisplayName"])
		logger.debug("    codingScheme: \"%s\"", self.m_DocumentEntry_eventCodeList["codingScheme"])

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		eventcodelist = E.Classification(
			E.Slot(
				E.ValueList(
					E.Value(self.m_DocumentEntry_eventCodeList["codingScheme"])
				),
				name = "codingScheme"
			),
			E.Name(
				E.LocalizedString(
					value = self.m_DocumentEntry_eventCodeList["codeDisplayName"]
				)
			),
			classificationScheme = "urn:uuid:2c6b8cb7-8b2a-4051-b291-b1ae6a575ef4",
			classifiedObject = self.documentEntry_entryUUID(),
			nodeRepresentation = self.m_DocumentEntry_eventCodeList["codeValue"],
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification",
			id = self.get_next_symbolic_id()
		)
		parentNode.append(eventcodelist)
		return


	# The code specifying the detailed technical format of the document. Along with the typeCode, it
	# should provide sufficient information to allow potential consumer to know if it will be able to
	# process the document.
	# The mimeType indicates the base format; the formatCode indicates the detailed-level technical
	# structure. Together with the mimeType, the formatCode used shall be sufficiently specific to
	# ensure processing/display by identifying a document encoding, structure and template (e.g., for a
	# CDA Document, the fact that it complies with a CDA schema, possibly a template and the choice
	# of a content-specific style sheet). The formatCode alone is often sufficiently specific, but an
	# actor that consumes metadata should not assume that it is.
	# The formatCode is often an indicator of the IHE Document Content Profile to which the
	# document conforms.
	# The mimeTypeSufficient formatCode of EV("urn:ihe:iti:xds:2017:mimeTypeSufficient",
	# "1.3.6.1.4.1.19376.1.2.3") may be used when the mimeType is sufficient to identify the technical
	# format of the document.
	# Format codes may be specified by multiple organizations. Format codes for Document Content
	# Profiles defined by the ITI domain shall be in URN format and have names with the prefix
	# urn:ihe:iti:
	# Format codes defined by other IHE domains shall have names with the prefix
	# urn:ihe:’domain initials’:
	# The IHE-managed codes and value set for formatCode are published on
	# http://wiki.ihe.net/index.php/IHE_Format_Codes.
	# Format codes defined by non-IHE domains should be a valid unique URN.
	#
	# Required
	#
	def DocumentEntry_formatCode(self, parentNode) :
		if not self.m_DocumentEntry_formatCode["codeValue"]:
			logger.error("Not creating DocumentEntry.formatCode as value is empty")
			raise RuntimeError("DocumentEntry.formatCode is a required field. Aborting XDS submission")

		logger.debug("DocumentEntry formatCode:")
		logger.debug("    codeValue: \"%s\"", self.m_DocumentEntry_formatCode["codeValue"])
		logger.debug("    codeDisplayName: \"%s\"", self.m_DocumentEntry_formatCode["codeDisplayName"])
		logger.debug("    codingScheme: \"%s\"", self.m_DocumentEntry_formatCode["codingScheme"])

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		formatcode = E.Classification(
			E.Slot(
				E.ValueList(
					E.Value(self.m_DocumentEntry_formatCode["codingScheme"])
				),
				name = "codingScheme"
			),
			E.Name(
				E.LocalizedString(
					value = self.m_DocumentEntry_formatCode["codeDisplayName"]
				)
			),
			classificationScheme = "urn:uuid:a09d5840-386c-46f2-b5ad-9c3699a4309d",
			classifiedObject = self.documentEntry_entryUUID(),
			nodeRepresentation = self.m_DocumentEntry_formatCode["codeValue"],
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification",
			id = self.get_next_symbolic_id()
		)
		parentNode.append(formatcode)
		return


	# The hash of the contents of the document.
	# The hash attribute can be used to identify accidental document corruption, mistaken duplicate
	# IDs, etc. The SHA1 algorithm and hash attribute should not be used for identifying malicious
	# alterations.
	#
	# Optional
	#
	def DocumentEntry_hash(self, parentNode) :
		if not self.m_DocumentEntry_hash:
			logger.warning("Not creating DocumentEntry.hash as value is empty")
			return

		logger.debug("DocumentEntry hash: \"%s\"", self.m_DocumentEntry_hash)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		hash = E.Slot(
			E.ValueList(
				E.Value(self.m_DocumentEntry_hash)
			)
		)
		parentNode.append(hash)
		return


	# This code represents the type of organizational setting of the clinical encounter during which the
	# documented act occurred.
	# In some cases, the setting of the encounter is inherent in the typeCode, such as "Diabetes Clinic
	# Progress Note". healthcareFacilityTypeCode shall be equivalent to or further specialize the value
	# inherent in the typeCode; for example, where the typeCode is simply "Clinic Progress Note" and
	# the value of healthcareFacilityTypeCode is "private clinic".
	#
	# Required
	#
	def DocumentEntry_healthcareFacilityTypeCode(self, parentNode) :
		if not self.m_DocumentEntry_healthcareFacilityTypeCode["codeValue"]:
			logger.error("Not creating DocumentEntry.healthcareFacilityTypeCode as value is empty")
			raise RuntimeError("DocumentEntry.healthcareFacilityTypeCode is a required field. Aborting XDS submission")

		logger.debug("DocumentEntry healthcareFacilityTypeCode:")
		logger.debug("    codeValue: \"%s\"", self.m_DocumentEntry_healthcareFacilityTypeCode["codeValue"])
		logger.debug("    codeDisplayName: \"%s\"", self.m_DocumentEntry_healthcareFacilityTypeCode["codeDisplayName"])
		logger.debug("    codingScheme: \"%s\"", self.m_DocumentEntry_healthcareFacilityTypeCode["codingScheme"])

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		healthcarefacilitytypecode = E.Classification(
			E.Slot(
				E.ValueList(
					E.Value(self.m_DocumentEntry_healthcareFacilityTypeCode["codingScheme"])
				),
				name = "codingScheme"
			),
			E.Name(
				E.LocalizedString(
					value = self.m_DocumentEntry_healthcareFacilityTypeCode["codeDisplayName"]
				)
			),
			classificationScheme = "urn:uuid:f33fb8ac-18af-42cc-ae0e-ed0b0bdb91e1",
			classifiedObject = self.documentEntry_entryUUID(),
			nodeRepresentation = self.m_DocumentEntry_healthcareFacilityTypeCode["codeValue"],
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification",
			id = self.get_next_symbolic_id()
		)
		parentNode.append(healthcarefacilitytypecode)
		return


	# A globally unique identifier for a community where the DocumentEntry and document can be
	# accessed.
	#
	# Optional
	#
	def DocumentEntry_homeCommunityId(self, parentNode) :
		if not self.m_DocumentEntry_homeCommunityId:
			logger.warning("Not creating DocumentEntry.homeCommunityId as value is empty")
			return

		logger.debug("DocumentEntry homeCommunityId: \"%s\"", self.m_DocumentEntry_homeCommunityId)

		parentNode.attrib['home'] = self.m_DocumentEntry_homeCommunityId
		return


	# Specifies the human language of character data in the document
	#
	# Required
	#
	def DocumentEntry_languageCode(self, parentNode) :
		if not self.m_DocumentEntry_languageCode:
			logger.error("Not creating DocumentEntry.languageCode as value is empty")
			raise RuntimeError("DocumentEntry.languageCode is a required field. Aborting XDS submission")

		logger.debug("DocumentEntry languageCode: \"%s\"", self.m_DocumentEntry_languageCode)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		languagecode = E.Slot(
			E.ValueList(
				E.Value(self.m_DocumentEntry_languageCode)
			),
			name = "languageCode"
		)
		parentNode.append(languagecode)
		return


	# Represents a participant within an authorInstitution who has legally authenticated or attested the
	# document. Legal authentication implies that a document has been signed manually or
	# electronically by the legalAuthenticator.
	# XCN format
	#
	# Optional
	#
	def DocumentEntry_legalAuthenticator(self, parentNode) :
		if not self.m_DocumentEntry_legalAuthenticator:
			logger.warning("Not creating DocumentEntry.legalAuthenticator as value is empty")
			return

		logger.debug("DocumentEntry legalAuthenticator: \"%s\"", self.m_DocumentEntry_legalAuthenticator)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		legalauthenticator = E.Slot(
			E.ValueList(
				E.Value(self.m_DocumentEntry_legalAuthenticator)
			),
			name = "legalAuthenticator"
		)
		parentNode.append(legalauthenticator)
		return


	# Indicates whether the Document Entry was created using the less rigorous requirements of
	# metadata as defined for the Metadata-Limited Document Source Actor.
	#
	# Forbidden
	#
	def DocumentEntry_limitedMetadata(self, parentNode) :
		logger.debug("Function not allowed")
		assert False

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		limitedmetadata = E.Classification(
			classifiedObject = "DocEntry",
			classificationNode = "urn:uuid:ab9b591b-83ab-4d03-8f5d-f93b1fb92e85"
		)
		parentNode.append(limitedmetadata)
		return


	# MIME type of the document in the Repository
	#
	# Required
	#
	def DocumentEntry_mimeType(self, parentNode) :
		if not self.m_DocumentEntry_mimeType:
			logger.error("Not creating DocumentEntry.mimeType as value is empty")
			raise RuntimeError("DocumentEntry.mimeType is a required field. Aborting XDS submission")

		logger.debug("DocumentEntry mimeType: \"%s\"", self.m_DocumentEntry_mimeType)

		parentNode.attrib['mimeType'] = self.m_DocumentEntry_mimeType
		return


	# The objectType attribute reflects the type of DocumentEntry. As described in Section 4.1.1, there
	# are two DocumentEntry types: Stable Document Entry and On-Demand Document Entry. A
	# Stable Document Entry contains metadata about an already created document available for
	# retrieval is a Document Entry and is designated by setting objectType equal to the UUID for
	# Stable (see Section 4.2.5.2 for the UUID). An On-Demand Document Entry contains metadata
	# which can be used to create an on-demand document which collects the latest, most recent
	# available information at the time of retrieval. It is designed by setting an objectType equal to the
	# UUID for on-demand (see Section 4.2.5.2 for the UUID).
	# The value of the objectType is coded in the objectType XML attribute on the ExtrinsicObject
	# representing the DocumentEntry. In the example below, the objectType is urn:uuid:7edca82f-
	# 054d-47f2-a032-9b2a5b5186c1 and reflects a stable DocumentEntry.
	#
	# Required
	#
	def DocumentEntry_objectType(self, parentNode) :
		if not (self.m_DocumentEntry_objectType == "urn:uuid:7edca82f-054d-47f2-a032-9b2a5b5186c1" \
			or self.m_DocumentEntry_objectType == "urn:uuid:34268e47-fdf5-41a6-ba33-82133c465248"):
			raise RuntimeError("DocumentEntry.objectType is not Stable Document Entry nor On-Demand Document Entry. Aborting XDS submission")

		logger.debug("DocumentEntry objectType: \"%s\"", self.m_DocumentEntry_objectType)

		parentNode.attrib['objectType'] = self.m_DocumentEntry_objectType
		return


	# The patientId represents the subject of care of the document. For XDS the patient identifier
	# domain is the XDS Affinity Domain Patient Identifier Domain (XAD-PID).
	# Within a submission request, the value of patientId of the DocumentEntries shall match that of
	# the SubmissionSet
	# The format of the patientId value is CX; see Table 4.2.3.1.7-2.
	# It shall contain two parts:
	# • Assigning Authority Domain Id (organization that issued the Id)
	# • An Id from the above Assigning Authority.
	# No other values are allowed, as specified for the CX type. Using HL7 terminology, no other
	# values are allowed in the components of the coded value, nor are further subcomponents
	# allowed.
	#
	# Required
	#
	def DocumentEntry_patientId(self, parentNode) :
		if not self.m_DocumentEntry_patientId:
			logger.error("Not creating DocumentEntry.patientId as value is empty")
			raise RuntimeError("DocumentEntry.patientId is a required field. Aborting XDS submission")

		# TODO: Should be improved to match exactly "j98789^^^&1.2.3.4.343.1&ISO"
		# TODO: Should we support all the type codes other than ISO ?
		if self.m_DocumentEntry_patientId[-4:] != "&ISO":
			raise RuntimeError("DocumentEntry.patientId must end in &ISO")

		logger.debug("DocumentEntry patientId: \"%s\"", self.m_DocumentEntry_patientId)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		patientid = E.ExternalIdentifier(
			E.Name(
				E.LocalizedString(
					value = "XDSDocumentEntry.patientId"
				)
			),
			identificationScheme = "urn:uuid:58a6f841-87b3-4a3e-92fd-a8ffeff98427",
			value = self.m_DocumentEntry_patientId,
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:ExternalIdentifier",
			id = self.get_next_symbolic_id(),
			registryObject = self.documentEntry_entryUUID()
		)
		parentNode.append(patientid)
		return


	# The code specifying the clinical specialty where the act that resulted in the document was
	# performed (e.g., Family Practice, Laboratory, Radiology). It is suggested that the creating entity
	# draws these values from a coding scheme providing a coarse level of granularity (about 10 to 100
	# entries).
	#
	# Required
	#
	def DocumentEntry_practiceSettingCode(self, parentNode) :
		if not self.m_DocumentEntry_practiceSettingCode["codeValue"]:
			logger.error("Not creating DocumentEntry.practiceSettingCode as value is empty")
			raise RuntimeError("DocumentEntry.practiceSettingCode is a required field. Aborting XDS submission")

		logger.debug("DocumentEntry practiceSettingCode:")
		logger.debug("    codeValue: \"%s\"", self.m_DocumentEntry_practiceSettingCode["codeValue"])
		logger.debug("    codeDisplayName: \"%s\"", self.m_DocumentEntry_practiceSettingCode["codeDisplayName"])
		logger.debug("    codingScheme: \"%s\"", self.m_DocumentEntry_practiceSettingCode["codingScheme"])

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		practicesettingcode = E.Classification(
			E.Slot(
				E.ValueList(
					E.Value(self.m_DocumentEntry_practiceSettingCode["codingScheme"])
				),
				name = "codingScheme"
			),
			E.Name(
				E.LocalizedString(
					value = self.m_DocumentEntry_practiceSettingCode["codeDisplayName"]
				)
			),
			classificationScheme = "urn:uuid:cccf5598-8b07-4b77-a05e-ae952c785ead",
			classifiedObject = self.documentEntry_entryUUID(),
			nodeRepresentation = self.m_DocumentEntry_practiceSettingCode["codeValue"],
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification",
			id = self.get_next_symbolic_id()
		)
		parentNode.append(practicesettingcode)
		return


	# These Identifiers may be internal or external identifiers, e.g., Identifiers may be Accession
	# Numbers, Order Numbers, Referral Request Identifiers, XDW Workflow Instance Identifiers,
	# etc. The referenceIdList contains Identifiers CXi encoded, as specified in Table 4.2.3.1.7-2.
	# Max length is 256 characters.
	# Coded as an ebRIM Slot. May have multiple values.
	#
	# Optional
	#
	def DocumentEntry_referenceIdList(self, parentNode) :
		if len(self.m_DocumentEntry_referenceIdList) == 0:
			logger.warning("Not creating DocumentEntry.referenceIdList as values are empty")
			return

		# Create a Slot
		referenceidlist = etree.Element(rim_prefix + "Slot", nsmap = nsmap_rim, name = "urn:ihe:iti:xds:2013:referenceIdList")
		# Create a ValueList
		valuelist = etree.SubElement(referenceidlist, rim_prefix + "ValueList")
		logger.debug("DocumentEntry referenceIdList:")
		for referenceid in self.m_DocumentEntry_referenceIdList:
			# Create one Value for each reference ID
			logger.debug("    Value: \"%s\"", referenceid)
			sub = etree.SubElement(valuelist, rim_prefix + "Value")
			sub.text = referenceid
		parentNode.append(referenceidlist)
		return


	# The globally unique, immutable, identifier of the repository where the document referenced by
	# the Document Entry can be accessed. This unique identifier for the repository may be used to
	# identify and connect to the specific repository to access the document
	#
	# Optional
	#
	def DocumentEntry_repositoryUniqueId(self, parentNode) :
		if not self.m_DocumentEntry_repositoryUniqueId:
			logger.warning("Not creating DocumentEntry.repositoryUniqueId as value is emtpy")
			return

		logger.debug("DocumentEntry repositoryUniqueId: \"%s\"", self.m_DocumentEntry_repositoryUniqueId)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		repositoryuniqueid = E.Slot(
			E.ValueList(
				E.Value(self.m_DocumentEntry_repositoryUniqueId)
			)
		)
		parentNode.append(repositoryuniqueid)
		return


	# Represents the start time of the service being documented (clinically significant, but not
	# necessarily when the document was produced or approved). This may be the same as the
	# encounter time in case the service was delivered during an encounter. Encounter time is not
	# coded in metadata but may be coded within the document.
	# Note: If needed, other times associated with the document, such as time of approval, are to be
	# recorded within the document.
	# The format of serviceStartTime value is DTM
	# TODO: Check date is valid
	#
	# Required if known
	#
	def DocumentEntry_serviceStartTime(self, parentNode) :
		if not self.m_DocumentEntry_serviceStartTime:
			logger.warning("Not creating DocumentEntry.serviceStartTime as value is emtpy")
			return

		logger.debug("DocumentEntry serviceStartTime: \"%s\"", self.m_DocumentEntry_serviceStartTime)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		servicestarttime = E.Slot(
			E.ValueList(
				E.Value(self.m_DocumentEntry_serviceStartTime)
			),
			name = "serviceStartTime"
		)
		parentNode.append(servicestarttime)
		return


	# Represents the stop time of the service being documented (clinically significant, but not
	# necessarily when the document was produced or approved). This may be the same as the
	# encounter time in case the service was delivered during an encounter. Encounter time is not
	# coded in metadata but may be coded within the document.
	# If the service happens at a point in time, this attribute shall contain the same value as the
	# serviceStartTime.
	# The format of serviceStopTime value is DTM
	# TODO: Check date is valid
	#
	# Required if known
	#
	def DocumentEntry_serviceStopTime(self, parentNode) :
		if not self.m_DocumentEntry_serviceStopTime:
			logger.warning("Not creating DocumentEntry.serviceStopTime as value is emtpy")
			return

		logger.debug("DocumentEntry serviceStopTime: \"%s\"", self.m_DocumentEntry_serviceStopTime)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		servicestoptime = E.Slot(
			E.ValueList(
				E.Value(self.m_DocumentEntry_serviceStopTime)
			),
			name = "serviceStopTime"
		)
		parentNode.append(servicestoptime)
		return


	# Size in bytes of the byte stream that comprises the document
	#
	# Optional
	#
	def DocumentEntry_size(self, parentNode) :
		if self.m_DocumentEntry_size == 0:
			logger.warning("Not creating DocumentEntry.size as value is 0")
			return

		logger.debug("DocumentEntry size: \"%s\"", self.m_DocumentEntry_size)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		documentsize = E.Slot(
			E.ValueList(
				E.Value(self.m_DocumentEntry_size)
			)
		)
		parentNode.append(documentsize)
		return


	# The sourcePatientId represents the subject of care’s medical record identifier (e.g., Patient Id) in
	# the local patient identifier domain of the creating entity.
	# Coded as an ebRIM Slot with the value encoded according the CX
	# datatype (see Table 4.2.3.1.7-2)
	#
	# Required
	#
	def DocumentEntry_sourcePatientId(self, parentNode) :
		if not self.m_DocumentEntry_sourcePatientId:
			logger.error("Not creating DocumentEntry.sourcePatientId as value is empty")
			raise RuntimeError("DocumentEntry.sourcePatientId is a required field. Aborting XDS submission")

		# TODO: Should be improved to match properly "j98789^^^&1.2.3.4.343.1&ISO"
		# TODO: Should we support all the type codes other than ISO ?
		if self.m_DocumentEntry_sourcePatientId[-4:] != "&ISO":
			raise RuntimeError("DocumentEntry.sourcePatientId must end in &ISO")

		logger.debug("DocumentEntry sourcePatientId: \"%s\"", self.m_DocumentEntry_sourcePatientId)

		# Create a "Slot"
		sourcepatientid = etree.Element(rim_prefix + "Slot", nsmap = nsmap_rim, name = "sourcePatientId")
		# Create a "ValueList"
		valuelist = etree.SubElement(sourcepatientid, rim_prefix + "ValueList")
		# Create a "Value"
		sub = etree.SubElement(valuelist, rim_prefix + "Value")
		sub.text = self.m_DocumentEntry_sourcePatientId
		parentNode.append(sourcepatientid)
		return


	# This attribute contains demographics information at the time of submission of the patient to
	# whose medical record this document belongs.
	# This information typically includes: the patient first and last name, sex, and birth date. Policies at
	# the creating entity may require more or less specific information and format.
	# This patient information is not intended to be updated once the document is registered (just as the
	# document content and metadata itself will not be updated without replacing the previous
	# document). As sourcePatientInfo may have been updated by the source actor, it may no longer be
	# in use within the Document Source (EHR-CR). It is only intended as an audit/checking
	# mechanism and has occasional use for Document Consumer Actors.
	# Coding:
	# Coded as an ebRIM Slot. If present, each rim:Value contains a Field (see Table 4.2.3.1.7-2 for a
	# description of the Field datatype). Multiple rim:Value elements may exist for the same field
	# name as a way to implement repetition; there shall be at most one rim:Value element for each of
	# the PID-7 and PID-8 fields. Only field defined for the PID segment shall be used.
	# Maximum length of each rim:Value is 256 characters. The sourcePatientInfo attribute should
	# include:
	# • PID-3 (source patient identifier list)
	# • PID-5 (source patient name)
	# • If multiple patient names are present, then PID-5.7 “Name Type Code” and PID-5.8
	#   “Name Representation Code” should be valued in each entry.
	# • PID-7 (source patient date of birth)
	# • PID-8 (source patient gender)
	# The sourcePatientInfo attribute should not include values for PID-2 (patient id), PID-4 (alternate
	# patient id), PID-12 (country code), or PID-19 (social security number).
	#
	# Optional
	#
	def DocumentEntry_sourcePatientInfo(self, parentNode) :
		if len(self.m_DocumentEntry_sourcePatientInfo) == 0:
			logger.warning("Not creating DocumentEntry.sourcePatientInfo as values are empty")
			return

		# Create a "Slot"
		sourcepatientinfo = etree.Element(rim_prefix + "Slot", nsmap = nsmap_rim, name = "sourcePatientInfo")
		# Create a "ValueList"
		valuelist = etree.SubElement(sourcepatientinfo, rim_prefix + "ValueList")
		logger.debug("DocumentEntry sourcePatientInfo:")
		for demographic in self.m_DocumentEntry_sourcePatientInfo:
			logger.debug("    Value: \"%s\"", demographic)
			# Create a "Value"
			sub = etree.SubElement(valuelist, rim_prefix + "Value")
			sub.text = demographic
		parentNode.append(sourcepatientinfo)
		return


	# Represents the title of the document.
	# Clinical documents often do not have a title; in such case the classCode (e.g., a "consultation" or
	# "progress note") is often used as the title. In that case, the title is usually omitted.
	#
	# Optional
	#
	def DocumentEntry_title(self, parentNode) :
		if not self.m_DocumentEntry_title:
			logger.warning("Not creating DocumentEntry.title as value is empty")
			return

		logger.debug("DocumentEntry title: \"%s\"", self.m_DocumentEntry_title)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		title = E.Name(
			E.LocalizedString(
				value = self.m_DocumentEntry_title
			)
		)
		parentNode.append(title)
		return


	# The code specifying the precise type of document from the user’s perspective. It is recommended
	# that the creating entity draw these values from a coding scheme providing a fine level of
	# granularity such as LOINC.
	#
	# Required
	#
	def DocumentEntry_typeCode(self, parentNode) :
		if not self.m_DocumentEntry_typeCode["codeValue"]:
			logger.error("Not creating DocumentEntry.typeCode as value is empty")
			raise RuntimeError("DocumentEntry.typeCode is a required field. Aborting XDS submission")

		logger.debug("DocumentEntry typeCode:")
		logger.debug("    codeValue: \"%s\"", self.m_DocumentEntry_typeCode["codeValue"])
		logger.debug("    codeDisplayName: \"%s\"", self.m_DocumentEntry_typeCode["codeDisplayName"])
		logger.debug("    codingScheme: \"%s\"", self.m_DocumentEntry_typeCode["codingScheme"])

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		typecode = E.Classification(
			E.Slot(
				E.ValueList(
					E.Value(self.m_DocumentEntry_typeCode["codingScheme"])
				),
				name = "codingScheme"
			),
			E.Name(
				E.LocalizedString(
					value = self.m_DocumentEntry_typeCode["codeDisplayName"]
				)
			),
			classificationScheme = "urn:uuid:f0306f51-975f-434e-a61c-c59651d33983",
			classifiedObject = self.documentEntry_entryUUID(),
			nodeRepresentation = self.m_DocumentEntry_typeCode["codeValue"],
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification",
			id = self.get_next_symbolic_id()
		)
		parentNode.append(typecode)
		return


	# Globally unique identifier assigned to the document by its creator
	# See section 4.2.3.2.26 DocumentEntry.uniqueId in ITI TF-3
	#
	# Required
	#
	def DocumentEntry_uniqueId(self, parentNode) :
		if not self.m_DocumentEntry_uniqueId["value"]:
			logger.error("Not creating DocumentEntry.uniqueId as value is empty")
			raise RuntimeError("DocumentEntry.uniqueId is a required field. Aborting XDS submission")

		logger.debug("DocumentEntry uniqueId: \"%s\"", self.documentEntry_entryUUID())

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		uniqueid = E.ExternalIdentifier(
			E.Name(
				E.LocalizedString(
					value = self.m_DocumentEntry_uniqueId["codeDisplayName"]
				)
			),
			identificationScheme = "urn:uuid:2e82c1f6-a085-4c72-9da3-8640a32e42ab",
			value = self.m_DocumentEntry_uniqueId["value"],
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:ExternalIdentifier",
			id = self.get_next_symbolic_id(),
			registryObject = self.documentEntry_entryUUID()
		)
		parentNode.append(uniqueid)
		return


	# The URI attribute contains the URI for the document.
	# Max length is 256 characters. Coded as an ebRIM Slot. Shall have only a single value.
	#
	# Optional
	#
	def DocumentEntry_URI(self, parentNode) :
		if not self.m_DocumentEntry_URI:
			logger.warning("Not creating DocumentEntry.URI as value is empty")
			return

		logger.debug("DocumentEntry URI: \"%s\"", self.m_DocumentEntry_URI)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		URI = E.Name(
			E.LocalizedString(
				value = self.m_DocumentEntry_URI
			)
		)
		parentNode.append(URI)
		return


	###################################################################
	## Submission Set
	###################################################################
	# SubmissionSet – metadata describing a collection of Folders, DocumentEntries, and
	# Associations submitted together.


	# Represents the humans and/or machines that authored the SubmissionSet. See Section 4.2.3.1.4
	# for details on creating the structure.
	# authorPerson – zero or one
	# authorInstitution – zero or more
	# authorRole – zero or more
	# authorSpecialty – zero or more
	# authorTelecommunication – zero or more
	#
	# Required if known
	#
	def SubmissionSet_author(self, parentNode) :
		if len(self.m_SubmissionSet_author) == 0:
			logger.warning("Not creating SubmissionSet.author as values are empty")
			return

		# For each author
		for author in self.m_SubmissionSet_author:
			logger.debug("SubmissionSet author:")
			# Create a Classification
			classification = etree.Element(rim_prefix + "Classification",
				nsmap = nsmap_rim,
				classificationScheme = "urn:uuid:a7058bb9-b4e4-4307-ba5b-e3f0ab85e12d",
				classifiedObject = self.submissionSet_entryUUID(),
				nodeRepresentation = "",
				objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification",
				id = self.get_next_symbolic_id()
			)
			# There is an authorvalue, authorrole pair
			for authorrole in author:
				# There is an authorvalue, authorrole pair
				slot = etree.SubElement(classification, rim_prefix + "Slot")
				logger.debug("    authorrole: \"%s\"", authorrole["authorrole"])
				slot.attrib['name'] = authorrole["authorrole"]
				valuelist = etree.SubElement(slot, rim_prefix + "ValueList")
				# authorvalue is an array
				for authorvalue in authorrole["authorvalue"]:
					sub = etree.SubElement(valuelist, rim_prefix + "Value")
					logger.debug("    authorvalue: \"%s\"", authorvalue)
					sub.text = authorvalue
			# Add this author to the list of authors
			parentNode.append(classification)
		return


	# Represents the status of the SubmissionSet. Since the deprecation of SubmissionSets is not
	# allowed, this value shall always be Approved.
	#
	# Optional
	#
	def SubmissionSet_availabilityStatus(self, parentNode) :
		# logger.debug("SubmissionSet availabilityStatus: \"%s\"", self.m_SubmissionSet_availabilityStatus)
		parentNode.attrib['status'] = "urn:oasis:names:tc:ebxml-regrep:StatusType:Approved"
		return


	# Contains comments associated with the SubmissionSet
	#
	# Optional
	#
	def SubmissionSet_comments(self, parentNode) :
		if not self.m_SubmissionSet_comments:
			logger.warning("Not creating SubmissionSet.comments as value is empty")
			return

		logger.debug("SubmissionSet comments: \"%s\"", self.m_SubmissionSet_comments)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		comments = E.Description(
			E.LocalizedString(
				value = self.m_SubmissionSet_comments
			)
		)
		parentNode.append(comments)
		return


	# The code specifying the type of clinical activity that resulted in placing these DocumentEntries,
	# Folders, and/or Associations in this SubmissionSet. These values are to be drawn from a
	# vocabulary defined by the creating entity that contributed the SubmissionSet.
	#
	# Required
	#
	def SubmissionSet_contentTypeCode(self, parentNode) :
		if not self.m_SubmissionSet_contentTypeCode["codeValue"]:
			logger.error("Not creating SubmissionSet.contentTypeCode as value is empty")
			raise RuntimeError("SubmissionSet.contentTypeCode is a required field. Aborting XDS submission")

		logger.debug("SubmissionSet contentTypeCode:")
		logger.debug("    codeValue: \"%s\"", self.m_SubmissionSet_contentTypeCode["codeValue"])
		logger.debug("    codeDisplayName: \"%s\"", self.m_SubmissionSet_contentTypeCode["codeDisplayName"])
		logger.debug("    codingScheme: \"%s\"", self.m_SubmissionSet_contentTypeCode["codingScheme"])

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		contenttypecode = E.Classification(
			E.Slot(
				E.ValueList(
					E.Value(self.m_SubmissionSet_contentTypeCode["codingScheme"])
				),
				name = "codingScheme"
			),
			E.Name(
				E.LocalizedString(
					value = self.m_SubmissionSet_contentTypeCode["codeDisplayName"]
				)
			),
			classificationScheme = "urn:uuid:aa543740-bdda-424e-8c96-df4873be8500",
			classifiedObject = self.submissionSet_entryUUID(),
			nodeRepresentation = self.m_SubmissionSet_contentTypeCode["codeValue"],
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification",
			id = self.get_next_symbolic_id()
		)
		parentNode.append(contenttypecode)
		return


	# The entryUUID attribute is a globally unique identifier primarily intended for internal document
	# management purposes. In contrast, the uniqueId attribute is used for external references (e.g.,
	# links, etc.).
	#
	# Required
	#
	def submissionSet_entryUUID(self) :
		if not self.m_SubmissionSet_entryUUID:
			logger.error("Not creating SubmissionSet.entryUUID as value is empty")
			raise RuntimeError("SubmissionSet.entryUUID is a required field. Aborting XDS submission")

		# logger.debug("SubmissionSet entryUUID: \"%s\"", self.m_SubmissionSet_entryUUID)

		return self.m_SubmissionSet_entryUUID


	# A globally unique identifier for a community.
	#
	# Optional
	#
	def SubmissionSet_homeCommunityId(self, parentNode) :
		if not self.m_SubmissionSet_homeCommunityId:
			logger.warning("Not creating SubmissionSet.homeCommunityId as value is empty")
			return

		logger.debug("SubmissionSet homeCommunityId: \"%s\"", self.m_SubmissionSet_homeCommunityId)

		parentNode.attrib['home'] = self.m_SubmissionSet_homeCommunityId
		return


	# Represents the organization(s) or person(s) for whom the SubmissionSet is intended at time of
	# submission. Each slot value shall include at least one of the organization, person, or
	# telecommunications address fields described below. It is highly recommended to define the
	# organization for all the persons, avoiding errors in the transmission of the documents
	# The value is coded as zero or more values within a single ebRIM Slot in the SubmissionSet.
	#
	# Optional
	#
	def SubmissionSet_intendedRecipient(self, parentNode) :
		if len(self.m_SubmissionSet_intendedRecipient) == 0:
			logger.warning("Not creating SubmissionSet.intendedRecipient as values are empty")
			return

		# Create a Slot
		intendedrecipient = etree.Element(rim_prefix + "Slot", nsmap = nsmap_rim, name = "intendedRecipient")
		# Create a ValueList
		valuelist = etree.SubElement(intendedrecipient, rim_prefix + "ValueList")
		for org_person in self.m_SubmissionSet_intendedRecipient:
			# Create one Value for each organization/person/telecommunications wntity
			logger.debug("SubmissionSet intendedRecipient: \"%s\"", org_person)
			sub = etree.SubElement(valuelist, rim_prefix + "Value")
			sub.text = org_person
		parentNode.append(intendedrecipient)
		return


	# Indicates whether the SubmissionSet was created using the less rigorous requirements of
	# metadata as defined for the Metadata-Limited Document Source
	#
	# Forbidden
	#
	def SubmissionSet_limitedMetadata(self, parentNode) :
		logger.debug("Function not allowed")
		assert False

		# logger.debug("SubmissionSet limitedMetadata: \"%s\"", self.m_SubmissionSet_limitedMetadata)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		limitedmetadata = E.Classification(
			classifiedObject = "SubmissionSet",
			classificationNode = "urn:uuid:5003a9db-8d8d-49e6-bf0c-990e34ac7707"
		)
		parentNode.append(limitedmetadata)
		return


	# The patientId represents the primary subject of care of the SubmissionSet
	# The format of the patientId value is CX (see Table 4.2.3.1.7-2)
	# It shall contain two parts:
	#    Assigning Authority Domain Id (organization that issued the Id).
	#    An Id from the above Assigning Authority.
	# No other values are allowed, as specified for the CX type. Using HL7 terminology, no other
	# values are allowed in the components of the coded value, nor are further subcomponents
	# allowed.
	#
	# Required
	#
	def SubmissionSet_patientId(self, parentNode) :
		if not self.m_SubmissionSet_patientId:
			logger.error("Not creating SubmissionSet.patientId as value is empty")
			raise RuntimeError("SubmissionSet.patientId is a required field. Aborting XDS submission")

		# TODO: Should be improved to match properly "j98789^^^&1.2.3.4.343.1&ISO"
		# TODO: Should we support all the type codes other than ISO ?
		if self.m_SubmissionSet_patientId[-4:] != "&ISO":
			raise RuntimeError("SubmissionSet.patientId must end in &ISO")

		logger.debug("SubmissionSet patientId: \"%s\"", self.m_SubmissionSet_patientId)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		patientid = E.ExternalIdentifier(
			E.Name(
				E.LocalizedString(
					value = "XDSSubmissionSet.patientId"
				)
			),
			identificationScheme = "urn:uuid:6b5aea1a-874d-4603-a4bc-96a0a7b38446",
			value = self.m_SubmissionSet_patientId,
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:ExternalIdentifier",
			id = self.get_next_symbolic_id(),
			registryObject = self.submissionSet_entryUUID()
		)
		parentNode.append(patientid)
		return


	# The globally unique, immutable, identifier of the entity that contributed the SubmissionSet.
	# When a "broker" is involved in sending SubmissionSets from a collection of client systems, it
	# shall use a different sourceId for submissions from each separate system to allow for tracking.
	#
	# Required
	#
	def SubmissionSet_sourceId(self, parentNode) :
		if not self.m_SubmissionSet_sourceId:
			logger.error("Not creating SubmissionSet.sourceId as value is empty")
			raise RuntimeError("SubmissionSet.sourceId is a required field. Aborting XDS submission")

		logger.debug("SubmissionSet sourceId: \"%s\"", self.m_SubmissionSet_sourceId)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		sourceid = E.ExternalIdentifier(
			E.Name(
				E.LocalizedString(
					value = "XDSSubmissionSet.sourceId"
				)
			),
			identificationScheme = "urn:uuid:554ac39e-e3fe-47fe-b233-965d2a147832",
			value = self.m_SubmissionSet_sourceId,
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:ExternalIdentifier",
			id = self.get_next_symbolic_id(),
			registryObject = self.submissionSet_entryUUID()
		)
		parentNode.append(sourceid)
		return


	# Represents the point in time at the creating entity when the SubmissionSet was created
	# This shall be provided by the submitting system
	# TODO: Check date is valid
	#
	# Required
	#
	def SubmissionSet_submissionTime(self, parentNode) :
		if not self.m_SubmissionSet_submissionTime:
			logger.error("Not creating SubmissionSet.submissionTime as value is empty")
			raise RuntimeError("SubmissionSet.submissionTime is a required field. Aborting XDS submission")

		logger.debug("SubmissionSet submissionTime: \"%s\"", self.m_SubmissionSet_submissionTime)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		submissiontime = E.Slot(
			E.ValueList(
				E.Value(self.m_SubmissionSet_submissionTime)
			),
			name = "submissionTime"
		)
		parentNode.append(submissiontime)
		return


	# Shall contain the title of the SubmissionSet
	#
	# Optional
	#
	def SubmissionSet_title(self, parentNode) :
		if not self.m_SubmissionSet_title:
			logger.warning("Not creating SubmissionSet.title as value is empty")
			return

		logger.debug("SubmissionSet title: \"%s\"", self.m_SubmissionSet_title)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		title = E.Name(
			E.LocalizedString(
				value = self.m_SubmissionSet_title
			)
		)
		parentNode.append(title)
		return


	# The globally unique identifier for the SubmissionSet assigned by the entity that contributed the
	# SubmissionSet
	#
	# Required
	#
	def SubmissionSet_uniqueId(self, parentNode) :
		if not self.m_SubmissionSet_uniqueId:
			logger.error("Not creating SubmissionSet.uniqueId as value is empty")
			raise RuntimeError("SubmissionSet.uniqueId is a required field. Aborting XDS submission")

		logger.debug("SubmissionSet uniqueId: \"%s\"", self.m_SubmissionSet_uniqueId)

		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		uniqueid = E.ExternalIdentifier(
			E.Name(
				E.LocalizedString(
					value = "XDSSubmissionSet.uniqueId"
				)
			),
			identificationScheme = "urn:uuid:96fdda7c-d067-4183-912e-bf5ee74998a8",
			value = self.m_SubmissionSet_uniqueId,
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:ExternalIdentifier",
			id = self.get_next_symbolic_id(),
			registryObject = self.submissionSet_entryUUID()
		)
		parentNode.append(uniqueid)
		return


	# A SubmissionSet object shall be created from a RegistryPackage element by labeling it with a
	#     Classification of type urn:uuid:a54d6aa5-d40d-43f9-88c5-b4633d873bdd
	#
	# Required
	#
	def create_SubmissionSet(self) :
		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		submissionset = E.Classification(
			classifiedObject = self.submissionSet_entryUUID(),
			classificationNode = "urn:uuid:a54d6aa5-d40d-43f9-88c5-b4633d873bdd",
			id = self.get_next_symbolic_id(),
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
		)
		return submissionset

	###################################################################
	## Folder
	###################################################################
	# Folder – metadata describing a collection of related DocumentEntries


	# Folder is not implemented


	###################################################################
	## Extrinsic Object
	###################################################################


	# DocumentEntry object type is modeled through the rim:ExtrinsicObject class
	#
	# Required
	#
	def build_ExtrinsicObject(self) :
		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		# Create "ExtrinsicObject"
		extrinsicobject = etree.Element(rim_prefix + "ExtrinsicObject", nsmap = nsmap_rim)

		# Add attributes
		extrinsicobject.attrib['id'] = self.documentEntry_entryUUID()
		self.DocumentEntry_mimeType(extrinsicobject)
		self.DocumentEntry_objectType(extrinsicobject)
		self.DocumentEntry_availabilityStatus(extrinsicobject)
		self.DocumentEntry_homeCommunityId(extrinsicobject)
		self.DocumentEntry_creationTime(extrinsicobject)
		self.DocumentEntry_languageCode(extrinsicobject)
		self.DocumentEntry_referenceIdList(extrinsicobject)
		self.DocumentEntry_legalAuthenticator(extrinsicobject)
		self.DocumentEntry_repositoryUniqueId(extrinsicobject)
		# TODO: Uncomment this!
		# May add optional self.m_DocumentEntry_hash(extrinsicobject)
		# May add optional self.m_DocumentEntry_size(extrinsicobject)
		self.DocumentEntry_serviceStartTime(extrinsicobject)
		self.DocumentEntry_serviceStopTime(extrinsicobject)
		self.DocumentEntry_sourcePatientId(extrinsicobject)
		self.DocumentEntry_sourcePatientInfo(extrinsicobject)
		self.DocumentEntry_title(extrinsicobject)
		self.DocumentEntry_comments(extrinsicobject)
		self.DocumentEntry_author(extrinsicobject)
		self.DocumentEntry_classCode(extrinsicobject)
		self.DocumentEntry_confidentialityCode(extrinsicobject)
		self.DocumentEntry_formatCode(extrinsicobject)
		self.DocumentEntry_healthcareFacilityTypeCode(extrinsicobject)
		self.DocumentEntry_practiceSettingCode(extrinsicobject)
		self.DocumentEntry_typeCode(extrinsicobject)
		self.DocumentEntry_patientId(extrinsicobject)
		self.DocumentEntry_uniqueId(extrinsicobject)
		return extrinsicobject


	###################################################################
	## Registry Package
	###################################################################


	def build_RegistryPackage(self) :
		# Create "RegistryPackage"
		registrypackage = etree.Element(rim_prefix + "RegistryPackage", nsmap = nsmap_rim)

		# Add attributes
		registrypackage.attrib['id'] = self.submissionSet_entryUUID()
		registrypackage.attrib['objectType'] = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:RegistryPackage"
		# May add optional SubmissionSet_availabilityStatus(registrypackage)
		self.SubmissionSet_homeCommunityId(registrypackage)
		self.SubmissionSet_submissionTime(registrypackage)
		self.SubmissionSet_title(registrypackage)
		self.SubmissionSet_comments(registrypackage)
		self.SubmissionSet_author(registrypackage)
		self.SubmissionSet_contentTypeCode(registrypackage)
		self.SubmissionSet_uniqueId(registrypackage)
		self.SubmissionSet_sourceId(registrypackage)
		self.SubmissionSet_patientId(registrypackage)
		self.SubmissionSet_intendedRecipient(registrypackage)
		# do NOT add Forbidden SubmissionSet_limitedMetadata(registrypackage)
		return registrypackage


	###################################################################
	## Association
	###################################################################


	# Association Types
	# Membership in a Registry Package (SubmissionSet or Folder)
	# 											urn:oasis:names:tc:ebxml-regrep:AssociationType:HasMember
	# Replace									urn:ihe:iti:2007:AssociationType:RPLC
	# Transformation							urn:ihe:iti:2007:AssociationType:XFRM
	# Addendum									urn:ihe:iti:2007:AssociationType:APND
	# Replace with Transformation				urn:ihe:iti:2007:AssociationType:XFRM_RPLC
	# Digital Signature							urn:ihe:iti:2007:AssociationType:signs
	# Snapshot of On-Demand document entry		urn:ihe:iti:2010:AssociationType:IsSnapshotOf

	# Membership in a Registry Package (SubmissionSet or Folder)
	def create_Association(self, associationtype) :
		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		association = E.Association(
			E.Slot(
				E.ValueList(
					E.Value("Original")
				),
				name = "SubmissionSetStatus"
			),
			associationType = associationtype,
			sourceObject = self.submissionSet_entryUUID(),
			targetObject = self.documentEntry_entryUUID(),
			id = self.get_next_symbolic_id(),
			objectType = "urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Association"
		)
		return association


	###################################################################
	## Registry Object List
	###################################################################


	def create_RegistryObjectList(self) :
		E = ElementMaker(namespace = nsmap_rim['rim'], nsmap = nsmap_rim)

		registryobjectlist = E.RegistryObjectList(
			self.build_ExtrinsicObject(),
			self.build_RegistryPackage(),
			self.create_SubmissionSet(),
			# Submission of an original Document (inclusion by value)
			# associationType = "urn:ihe:iti:2007:AssociationType:RPLC"
			# associationType = "urn:ihe:iti:2007:AssociationType:XFRM"
			# associationType = "urn:ihe:iti:2007:AssociationType:APND"
			# associationType = "urn:ihe:iti:2007:AssociationType:XFRM_RPLC"
			# associationType = "urn:ihe:iti:2007:AssociationType:signs"
			# associationType = "urn:ihe:iti:2010:AssociationType:IsSnapshotOf"
			self.create_Association("urn:oasis:names:tc:ebxml-regrep:AssociationType:HasMember")
		)
		return registryobjectlist


	###################################################################
	## Registry Object List
	###################################################################


	def create_Document(self, attachment_id) :
		# Create Document
		document = etree.Element(xdsb_prefix + "Document", nsmap = nsmap_xdsb)
		document.attrib['id'] = self.documentEntry_entryUUID()
		attachment = etree.SubElement(document, xop_prefix + "Include", nsmap = nsmap_xop)
		attachment.attrib['href'] = "cid:" + attachment_id
		return document


	###################################################################
	## Provide and Register DocumentSet Request
	###################################################################


	def build_ProvideAndRegisterDocumentSetRequest(self, hl7message, content_id1, attachment_id, attachment_hash, attachment_size) :

		logger.info("Building Provide And Register DocumentSet Request")

		self.m_DocumentEntry_size = attachment_size
		self.m_DocumentEntry_hash = attachment_hash

		# Fill all fiels with information. Usually imported from HL7 message
		self.fill_xds_metadata(hl7message)

		CD = etree.Element(xdsb_prefix + 'ProvideAndRegisterDocumentSetRequest', nsmap = nsmap_xdsb)
		E = ElementMaker(namespace = nsmap_lcm['lcm'], nsmap = nsmap_lcm)
		CD.append(
			E.SubmitObjectsRequest(
				self.create_RegistryObjectList()
			)
		)
		CD.append(
			self.create_Document(attachment_id)
		)

		# Log the whole XDS request
		# etree.indent(CD, space = "    ")
		logger.debug('Full XDS request here:{}{}'.format(os.linesep,
			etree.tostring(CD, pretty_print = True, xml_declaration = False, encoding = 'unicode'))
		)
		# etree.indent(CD, space = "  ")

		# XDS request file logging
		if config.LOG_XDS_REQUEST_TOFILE:
			if not os.path.exists(config.LOG_DIR_PATH + '/xds_requests') :
				os.makedirs(config.LOG_DIR_PATH + '/xds_requests')
			xdsreq_file_log = config.LOG_DIR_PATH + "/xds_requests/XDS_{}.xml".format(content_id1)
			logger.info("Writing XDS request to log file {}".format(xdsreq_file_log))
			text_file = open(xdsreq_file_log, "wb")
			# etree.indent(xds_request_tree, space = "    ")
			text_file.write(etree.tostring(CD, pretty_print = True, xml_declaration = False, encoding = 'utf-8'))
			text_file.close()

		# The actual lxml tree is returned
		return CD


if __name__ == "__main__":
	# For debugging purposes. Currently not working.
	CD = IheXds.build_ProvideAndRegisterDocumentSetRequest("fake", "cid:1.urn:uuid:566EAD10FEBB55C5A61257193478499@apache.org")
	etree.indent(CD, space = "    ")
	print(etree.tostring(CD, pretty_print = config.PRETTY_PRINT, encoding = 'unicode'))
