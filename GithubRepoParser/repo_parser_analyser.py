import os
import sys
import argparse
import configparser
from github import Github, GithubException
from repo_parser_analyser_service import (
    setup_logging, parse_github_url, get_repo_structure, 
    read_file_content, parse_gradle_file, parse_maven_file, write_analysis
)
from constants.app_constants import *
from constants.app_message_constants import *

def load_config(config_file_path: str):
    """Load configuration file"""
    config = configparser.ConfigParser()
    try:
        if os.path.exists(config_file_path):
            config.read(config_file_path)
            print(INFO_USING_CONFIG_FILE.format(config_file_path))
            return config if config.sections() else None
        else:
            print(WARNING_CONFIG_FILE_NOT_FOUND.format(config_file_path))
            return None
    except Exception as e:
        print(ERROR_CONFIG_LOADING.format(e))
        return None

def connect_to_github(github_token: str, repo_owner: str, repo_name: str, debug_logger, error_logger):
    """Connect to GitHub and get repository object"""
    try:
        g = Github(github_token)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        debug_logger.debug(DEBUG_CONNECTED_TO_REPO.format(repo.full_name))
        return repo
    except GithubException as e:
        error_logger.error(ERROR_GITHUB_API_READING_FILE.format('repository', e.status, e.data.get('message', '')))
        print(ERROR_GITHUB_API.format(e.status))
        sys.exit(1)
    except Exception as e:
        error_logger.error(ERROR_CONNECTION.format(e))
        print(ERROR_CONNECTION.format(e))
        sys.exit(1)

def print_summary(repo, structure: list, build_info: dict, output_dir: str):
    """Print analysis summary"""
    print(SUMMARY_HEADER)
    print(SUMMARY_REPOSITORY.format(repo.full_name))
    print(SUMMARY_STRUCTURE_ITEMS.format(len(structure)))
    
    if build_info:
        print(SUMMARY_BUILD_FILE_ANALYSIS)
        for key, value in build_info.items():
            print(SUMMARY_BUILD_ITEM.format(key, value))
    else:
        print(SUMMARY_NO_BUILD_INFO)
    
    print(INFO_FILES_CREATED.format(output_dir))
    print(FILE_LIST_MAIN_ANALYSIS.format(REPO_ANALYSIS_FILE))
    print(FILE_LIST_DEBUG_INFO.format(DEBUG_LOG_FILE))
    print(FILE_LIST_ERROR_INFO.format(ERROR_LOG_FILE))

def determine_repository(args, config):
    """Determine repository owner and name from arguments or config"""
    repo_owner = repo_name = None
    
    # Priority 1: Command line URL
    if args.url:
        try:
            repo_owner, repo_name = parse_github_url(args.url)
            return repo_owner, repo_name
        except ValueError as e:
            print(ERROR_INVALID_URL.format(e))
            sys.exit(1)
    
    # Priority 2: Command line owner and name
    if args.owner and args.name:
        return args.owner, args.name
    
    # Priority 3: Command line owner or name with config fallback
    if args.owner or args.name:
        if config and GITHUB_CONFIG_SECTION in config:
            repo_owner = args.owner or config.get(GITHUB_CONFIG_SECTION, CONFIG_REPO_OWNER, fallback=None)
            repo_name = args.name or config.get(GITHUB_CONFIG_SECTION, CONFIG_REPO_NAME, fallback=None)
        else:
            repo_owner = args.owner
            repo_name = args.name
    
    # Priority 4: Config file
    elif config and GITHUB_CONFIG_SECTION in config:
        repo_url = config.get(GITHUB_CONFIG_SECTION, CONFIG_REPO_URL, fallback=None)
        if repo_url:
            try:
                repo_owner, repo_name = parse_github_url(repo_url)
                return repo_owner, repo_name
            except ValueError:
                # If URL parsing fails, try individual values
                pass
        
        repo_owner = config.get(GITHUB_CONFIG_SECTION, CONFIG_REPO_OWNER, fallback=None)
        repo_name = config.get(GITHUB_CONFIG_SECTION, CONFIG_REPO_NAME, fallback=None)
    
    if not repo_owner or not repo_name:
        print(ERROR_REPOSITORY_NOT_SPECIFIED)
        sys.exit(1)
    
    return repo_owner, repo_name

def determine_build_type(args, config):
    """Determine build type from arguments or config"""
    build_type = args.build_type
    
    if not build_type and config and GITHUB_CONFIG_SECTION in config:
        build_type = config.get(GITHUB_CONFIG_SECTION, CONFIG_BUILD_TYPE, fallback=None)
    
    if not build_type:
        print(INFO_BUILD_TYPE_NOT_PROVIDED)
        build_type = 'gradle'
    
    # Check if unsupported build type
    if build_type not in ['gradle', 'maven']:
        print(WARNING_UNSUPPORTED_BUILD_TYPE.format(build_type))
        print(INFO_ONLY_GRADLE_MAVEN_SUPPORTED)
        print(INFO_SKIPPING_BUILD_FILE_ANALYSIS)
        return None  # Skip build file processing
    
    return build_type

def find_build_file(repo, build_type, debug_logger):
    """Automatically find build file based on build type"""
    build_files = {
        'gradle': ['build.gradle', 'build.gradle.kts'],
        'maven': ['pom.xml']
    }
    
    if build_type not in build_files:
        return None
    
    for file_name in build_files[build_type]:
        try:
            repo.get_contents(file_name)
            debug_logger.debug(f"Found build file: {file_name}")
            # Print the absolute build file path
            absolute_path = os.path.abspath(file_name)
            print(f"build_file_path: {absolute_path}")
            debug_logger.debug(f"BUILD_FILE_PATH: {absolute_path}")
            return file_name
        except:
            continue
    
    debug_logger.debug(f"No {build_type} build file found in root directory")
    return None

def determine_config_file_path(args):
    """Determine the configuration file path"""
    if args.config_file:
        # If config file specified, look in additional-configs directory
        config_path = os.path.join(ADDITIONAL_CONFIGS_DIR, args.config_file)
        if not config_path.endswith('.ini'):
            config_path += '.ini'
        return config_path
    else:
        # Default config file in root directory
        return CONFIG_FILE

def main():
    parser = argparse.ArgumentParser(description='GitHub Repository Analyzer')
    parser.add_argument('--token', '-t', help='GitHub token')
    parser.add_argument('--url', '-u', help='GitHub repository URL')
    parser.add_argument('--owner', '-o', help='Repository owner')
    parser.add_argument('--name', '-n', help='Repository name')
    parser.add_argument('--build-type', '-b', choices=['gradle', 'maven'], 
                       help='Build system type (default: gradle)')
    parser.add_argument('--config-file', '-c', help='Configuration file name in additional-configs directory')
    
    args = parser.parse_args()
    
    # Use default output directory
    output_dir = OUTPUT_DIR
    
    # Setup logging
    debug_logger, error_logger = setup_logging(output_dir)
    debug_logger.debug(DEBUG_STARTING_ANALYSIS)
    
    # Get GitHub token
    github_token = args.token or os.environ.get(GITHUB_TOKEN_ENV_VAR)
    if not github_token:
        error_logger.error(ERROR_GITHUB_TOKEN_NOT_PROVIDED)
        print(ERROR_GITHUB_TOKEN_REQUIRED)
        sys.exit(1)
    
    # Determine config file path and load config
    config_file_path = determine_config_file_path(args)
    config = load_config(config_file_path)
    
    # Determine repository
    repo_owner, repo_name = determine_repository(args, config)
    
    # Determine build type
    build_type = determine_build_type(args, config)
    
    debug_logger.debug(DEBUG_REPOSITORY_INFO.format(repo_owner, repo_name))
    debug_logger.debug(DEBUG_BUILD_TYPE_INFO.format(build_type))
    
    print(INFO_ANALYZING_REPO.format(repo_owner, repo_name))
    if build_type:
        print(INFO_BUILD_TYPE.format(build_type))
    else:
        print(INFO_BUILD_FILE_ANALYSIS_SKIPPED)
    print(INFO_OUTPUT_DIRECTORY.format(output_dir))
    
    # Connect to GitHub
    repo = connect_to_github(github_token, repo_owner, repo_name, debug_logger, error_logger)
    
    # Get repository structure
    structure = get_repo_structure(repo, debug_logger)
    
    # Read and parse build file
    build_info = {}
    if build_type:
        build_file = find_build_file(repo, build_type, debug_logger)
        if build_file:
            print(INFO_BUILD_FILE.format(build_file))
            debug_logger.debug(DEBUG_BUILD_FILE_INFO.format(build_file))
            try:
                content = read_file_content(repo, build_file, debug_logger, error_logger)
                if content:
                    if build_type == 'gradle':
                        build_info = parse_gradle_file(content, debug_logger)
                    elif build_type == 'maven':
                        build_info = parse_maven_file(content, debug_logger)
                else:
                    print(WARNING_COULD_NOT_READ_BUILD_FILE.format(build_file))
            except FileNotFoundError as e:
                error_logger.error(str(e))
                sys.exit(1)
            except Exception as e:
                error_logger(f"Unexpected error accessing build file: {str(e)}")
                sys.exit(1)
        else:
            print(WARNING_BUILD_FILE_NOT_FOUND.format(build_type))
    
    # Write analysis
    write_analysis(repo, structure, build_info, output_dir)
    
    # Print summary
    print_summary(repo, structure, build_info, output_dir)
    
    debug_logger.debug(DEBUG_ANALYSIS_COMPLETED)

if __name__ == "__main__":
    main()

# Usage Examples:
# Basic usage - everything from config
# python repo_parser_analyser.py --token YOUR_TOKEN

# Override build type
# python repo_parser_analyser.py --token YOUR_TOKEN --build-type maven
# python repo_parser_analyser.py --token YOUR_TOKEN --build-type gradle

# Specify repository URL
# python repo_parser_analyser.py --token YOUR_TOKEN --url https://github.com/owner/repo

# Specify repository owner and name
# python repo_parser_analyser.py --token YOUR_TOKEN --owner pulak-code --name poc

# Specify only owner (name from config)
# python repo_parser_analyser.py --token YOUR_TOKEN --owner pulak-code

# Specify only name (owner from config)
# python repo_parser_analyser.py --token YOUR_TOKEN --name poc

# Use custom config file
# python repo_parser_analyser.py --token YOUR_TOKEN --config-file custom_config.ini

# Full specification with custom config
# python repo_parser_analyser.py --token YOUR_TOKEN --owner pulak-code --name poc --build-type gradle --config-file custom_config.ini