# Application Constants

# Configuration
CONFIG_FILE = 'config.ini'
ADDITIONAL_CONFIGS_DIR = 'additional-configs'
GITHUB_CONFIG_SECTION = 'github'
CONFIG_REPO_OWNER = 'repo_owner'
CONFIG_REPO_NAME = 'repo_name'
CONFIG_REPO_URL = 'repo_url'
CONFIG_BUILD_TYPE = 'build_type'
CONFIG_FILE_TO_READ = 'file_to_read'

# Environment Variables
GITHUB_TOKEN_ENV_VAR = 'GITHUB_TOKEN'

# Output
OUTPUT_DIR = 'output'
REPO_ANALYSIS_FILE = 'repo_analysis.txt'
DEBUG_LOG_FILE = 'debug.log'
ERROR_LOG_FILE = 'error.log'

# File Structure Prefixes
DIRECTORY_PREFIX = "📁"
FILE_PREFIX = "📄"

# Default Values
DEFAULT_DESCRIPTION = "No description available"
DEFAULT_LANGUAGE = "Not specified"

# Analysis Headers
ANALYSIS_HEADER_REPO = "=" * 50 + "\nREPOSITORY ANALYSIS\n" + "=" * 50
ANALYSIS_HEADER_STRUCTURE = "\n" + "=" * 50 + "\nREPOSITORY STRUCTURE\n" + "=" * 50
ANALYSIS_HEADER_BUILD = "\n" + "=" * 50 + "\nBUILD FILE ANALYSIS\n" + "=" * 50

# Analysis Content
ANALYSIS_REPO_NAME = "Repository: {}"
ANALYSIS_REPO_URL = "URL: {}"
ANALYSIS_REPO_DESCRIPTION = "Description: {}"
ANALYSIS_REPO_LANGUAGE = "Primary Language: {}"
ANALYSIS_REPO_STATS = "Stars: {} | Forks: {}"