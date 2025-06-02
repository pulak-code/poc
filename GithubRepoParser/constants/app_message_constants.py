# Message Constants

# Error Messages
ERROR_CONFIG_LOADING = "Error loading configuration file: {}"
ERROR_GITHUB_TOKEN_NOT_PROVIDED = "GitHub token not provided"
ERROR_GITHUB_TOKEN_REQUIRED = "GitHub token is required. Provide via --token argument or GITHUB_TOKEN environment variable."
ERROR_GITHUB_API = "GitHub API Error: {}"
ERROR_GITHUB_API_READING_FILE = "GitHub API error reading {}: Status {}, Message: {}"
ERROR_CONNECTION = "Connection error: {}"
ERROR_INVALID_URL = "Invalid GitHub URL: {}"
ERROR_REPOSITORY_NOT_SPECIFIED = "Repository not specified. Provide via --url, --owner/--name arguments, or config file."
ERROR_REPO_STRUCTURE = "Error getting repository structure: {}"
ERROR_READING_FILE = "Error reading file {}: {}"
ERROR_CONFIG_FILE_NOT_FOUND = "Config file not found: {}"

# Warning Messages
WARNING_UNSUPPORTED_BUILD_TYPE = "Warning: Unsupported build type '{}'"
WARNING_COULD_NOT_READ_BUILD_FILE = "Warning: Could not read build file: {}"
WARNING_BUILD_FILE_NOT_FOUND = "Warning: No {} build file found in repository root"
WARNING_CONFIG_FILE_NOT_FOUND = "Warning: Config file '{}' not found, using command line arguments only"

# Info Messages
INFO_BUILD_TYPE_NOT_PROVIDED = "Build type not provided, defaulting to 'gradle'"
INFO_ONLY_GRADLE_MAVEN_SUPPORTED = "Only 'gradle' and 'maven' build types are currently supported"
INFO_SKIPPING_BUILD_FILE_ANALYSIS = "Skipping build file analysis"
INFO_ANALYZING_REPO = "Analyzing repository: {}/{}"
INFO_BUILD_TYPE = "Build type: {}"
INFO_BUILD_FILE_ANALYSIS_SKIPPED = "Build file analysis: Skipped (unsupported build type)"
INFO_OUTPUT_DIRECTORY = "Output directory: {}"
INFO_BUILD_FILE = "Build file found: {}"
INFO_FILES_CREATED = "Analysis files created in: {}"
INFO_ANALYSIS_WRITTEN = "Analysis written to: {}"
INFO_USING_CONFIG_FILE = "Using config file: {}"

# Debug Messages
DEBUG_STARTING_ANALYSIS = "Starting repository analysis"
DEBUG_CONNECTED_TO_REPO = "Connected to repository: {}"
DEBUG_REPOSITORY_INFO = "Repository: owner={}, name={}"
DEBUG_BUILD_TYPE_INFO = "Build type: {}"
DEBUG_BUILD_FILE_INFO = "Build file: {}"
DEBUG_GETTING_REPO_STRUCTURE = "Getting repository structure"
DEBUG_SKIPPED_DIRECTORY = "Skipped directory (access denied): {}"
DEBUG_FOUND_ITEMS = "Found {} items in repository structure"
DEBUG_READING_FILE = "Reading file: {}"
DEBUG_SUCCESSFULLY_READ = "Successfully read {} characters from {}"
DEBUG_PARSING_GRADLE = "Parsing Gradle build file"
DEBUG_PARSING_MAVEN = "Parsing Maven POM file"
DEBUG_FOUND_PATTERN = "Found {}: {}"
DEBUG_ANALYSIS_COMPLETED = "Repository analysis completed successfully"

# Summary Messages
SUMMARY_HEADER = "\n" + "=" * 60 + "\nANALYSIS SUMMARY\n" + "=" * 60
SUMMARY_REPOSITORY = "Repository: {}"
SUMMARY_STRUCTURE_ITEMS = "Structure items found: {}"
SUMMARY_BUILD_FILE_ANALYSIS = "Build file analysis:"
SUMMARY_BUILD_ITEM = "  {}: {}"
SUMMARY_NO_BUILD_INFO = "Build file analysis: No information extracted"

# File List Messages
FILE_LIST_MAIN_ANALYSIS = "  📄 {} (main analysis)"
FILE_LIST_DEBUG_INFO = "  📄 {} (debug information)"
FILE_LIST_ERROR_INFO = "  📄 {} (error log)"