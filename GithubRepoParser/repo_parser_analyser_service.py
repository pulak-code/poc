import re
import os
from github import Repository, GithubException
from typing import Dict, Tuple, List
from urllib.parse import urlparse
import logging
from constants.app_constants import *
from constants.app_message_constants import *

def setup_logging(output_dir: str):
    """Setup separate loggers for debug and error"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Debug logger
    debug_logger = logging.getLogger('debug')
    debug_logger.setLevel(logging.DEBUG)
    debug_handler = logging.FileHandler(os.path.join(output_dir, DEBUG_LOG_FILE), mode='w')
    debug_handler.setFormatter(logging.Formatter('%(asctime)s - DEBUG - %(message)s'))
    debug_logger.addHandler(debug_handler)
    
    # Error logger
    error_logger = logging.getLogger('error')
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.FileHandler(os.path.join(output_dir, ERROR_LOG_FILE), mode='w')
    error_handler.setFormatter(logging.Formatter('%(asctime)s - ERROR - %(message)s'))
    error_logger.addHandler(error_handler)
    
    return debug_logger, error_logger

def parse_github_url(url: str) -> Tuple[str, str]:
    """Parse GitHub URL to extract owner and repo name"""
    try:
        parsed = urlparse(url)
        if parsed.netloc != 'github.com':
            raise ValueError("Not a GitHub URL")
        
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub URL format")
        
        owner, repo = path_parts[0], path_parts[1]
        if repo.endswith('.git'):
            repo = repo[:-4]
        
        return owner, repo
    except Exception as e:
        raise ValueError(f"Invalid GitHub URL: {url}")

def get_repo_structure(repo: Repository, debug_logger) -> List[str]:
    """Get repository structure"""
    debug_logger.debug(DEBUG_GETTING_REPO_STRUCTURE)
    structure = []
    
    try:
        contents = repo.get_contents("")
        queue = list(contents)
        processed = set()
        
        while queue:
            item = queue.pop(0)
            if item.path in processed:
                continue
            processed.add(item.path)
            
            if item.type == "dir":
                structure.append(f"{DIRECTORY_PREFIX}{item.path}/")
                try:
                    queue.extend(repo.get_contents(item.path))
                except GithubException:
                    debug_logger.debug(DEBUG_SKIPPED_DIRECTORY.format(item.path))
            else:
                structure.append(f"{FILE_PREFIX} {item.path}")
        
        debug_logger.debug(DEBUG_FOUND_ITEMS.format(len(structure)))
        return structure
        
    except Exception as e:
        debug_logger.error(ERROR_REPO_STRUCTURE.format(e))
        return []

def read_file_content(repo: Repository, file_path: str, debug_logger, error_logger) -> str:
    """Read content of a specific file"""
    if not file_path:
        return ""
    
    debug_logger.debug(DEBUG_READING_FILE.format(file_path))
    try:
        file_obj = repo.get_contents(file_path)
        content = file_obj.decoded_content.decode('utf-8')
        debug_logger.debug(DEBUG_SUCCESSFULLY_READ.format(len(content), file_path))
        return content
    except GithubException as e:
        error_logger.error(ERROR_GITHUB_API_READING_FILE.format(file_path, e.status, e.data.get('message', '')))
    except Exception as e:
        error_logger.error(f"File not found: {file_path} in the repository. Exception: {str(e)}")
        raise FileNotFoundError(f"Specified file '{file_path}' does not exist in the repository.")
    return ""

def parse_gradle_file(content: str, debug_logger) -> Dict:
    """Parse Gradle file for essential information"""
    debug_logger.debug(DEBUG_PARSING_GRADLE)
    
    if not content:
        return {}
    
    extracted = {}
    patterns = {
        'version': r"version\s*[=:]\s*['\"]([^'\"]+)['\"]",
        'group': r"group\s*[=:]\s*['\"]([^'\"]+)['\"]",
        'name': r"name\s*[=:]\s*['\"]([^'\"]+)['\"]",
        'description': r"description\s*[=:]\s*['\"]([^'\"]+)['\"]",
        'build_number': r"buildNumber\s*=\s*(\d+)",
        'project_owner': r"projectOwner\s*=\s*['\"]([^'\"]+)['\"]"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            value = match.group(1)
            if key == 'build_number':
                try:
                    value = int(value)
                except ValueError:
                    pass
            extracted[key] = value
            debug_logger.debug(DEBUG_FOUND_PATTERN.format(key, value))
    
    return extracted

def parse_maven_file(content: str, debug_logger) -> Dict:
    """Basic Maven POM parsing"""
    debug_logger.debug(DEBUG_PARSING_MAVEN)
    
    if not content:
        return {}
    
    extracted = {}
    patterns = {
        'group': r"<groupId>([^<]+)</groupId>",
        'name': r"<artifactId>([^<]+)</artifactId>",
        'version': r"<version>([^<]+)</version>",
        'description': r"<description>([^<]+)</description>"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            extracted[key] = match.group(1).strip()
            debug_logger.debug(DEBUG_FOUND_PATTERN.format(key, extracted[key]))
    
    return extracted

def write_analysis(repo: Repository, structure: List[str], build_info: Dict, output_dir: str):
    """Write analysis to file"""
    os.makedirs(output_dir, exist_ok=True)
    analysis_file = os.path.join(output_dir, REPO_ANALYSIS_FILE)
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        f.write(f"{ANALYSIS_HEADER_REPO}\n")
        f.write(f"{ANALYSIS_REPO_NAME.format(repo.full_name)}\n")
        f.write(f"{ANALYSIS_REPO_URL.format(repo.html_url)}\n")
        f.write(f"{ANALYSIS_REPO_DESCRIPTION.format(repo.description or DEFAULT_DESCRIPTION)}\n")
        f.write(f"{ANALYSIS_REPO_LANGUAGE.format(repo.language or DEFAULT_LANGUAGE)}\n")
        f.write(f"{ANALYSIS_REPO_STATS.format(repo.stargazers_count, repo.forks_count)}\n\n")
        
        f.write(f"{ANALYSIS_HEADER_STRUCTURE}\n")
        for item in structure:
            f.write(f"{item}\n")
        
        if build_info:
            f.write(f"{ANALYSIS_HEADER_BUILD}\n")
            for key, value in build_info.items():
                f.write(f"{key}: {value}\n")
    
    print(INFO_ANALYSIS_WRITTEN.format(analysis_file))