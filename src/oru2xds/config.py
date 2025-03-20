#
# Antonio Martins (digiplan.pt@gmail.com)
#

#
## oru2xds global configuration variables
#
APP_NAME = 'oru2xds'

# AFFINITY_DOMAIN_ASSIGNING_AUTHORITY_OID = "1.1.4567332.1.1"
AFFINITY_DOMAIN_ASSIGNING_AUTHORITY_OID = "1.3.6.1.4.1.21367.13.20.3000"

# XDS Provide and Register Document Set-b transaction endpoint
SERVICE_URL = "http://localhost:8084/xdstools7/sim/default__1/rep/prb"

# HL7 listening port
HL7_LISTENER_PORT = 2575

# Sending application and sending facility in HL7 reply messages
# leave None if you do not want to set them
HL7_MY_SENDING_APP = "ORU2XDS"
HL7_MY_SENDING_FACILITY = None

# Whether you want every CDA to be logged to a separate file
LOG_CDA_TOFILE = True

# Whether you want every XDS request to be logged to a separate file
LOG_XDS_REQUEST_TOFILE = True

# Whether you want every SOAP envelope to be logged to a separate file
LOG_SOAP_ENVELOPE_TOFILE = True

# Whether you want every SOAP response to be logged to a separate file
LOG_SOAP_RESPONSE_TOFILE = True

# HTTP user-agent string used in SOAP transaction
# TODO: update the user agent version from __version__.py
HTTP_USER_AGENT = 'oru2xds/1.0.0'

# If you want to add an xml stylesheet to the CDA, add it here
# cda_stylesheet = "CDA.xsl"
cda_stylesheet = None

# XML structures are sent with leading spaces in pretty_print or not
PRETTY_PRINT = True

# Logging
# Levels may be DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL_CONSOLE = "INFO"
LOG_LEVEL_FILE = "DEBUG"
# Do NOT set this variable. It will be set at runtime
LOG_DIR_PATH = None
