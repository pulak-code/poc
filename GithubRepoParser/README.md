# GitHub Repository Parser & Analyzer

A Python tool for analyzing GitHub repositories, extracting repository structure, and parsing build files (Gradle/Maven).

## Features

- 📁 **Repository Structure Analysis**: Complete directory and file structure extraction
- 🔧 **Build File Parsing**: Support for Gradle (`build.gradle`, `build.gradle.kts`) and Maven (`pom.xml`)
- 📊 **Detailed Reporting**: Comprehensive analysis with repository metadata
- 🔍 **Flexible Configuration**: Multiple ways to specify repositories and settings
- 📝 **Comprehensive Logging**: Debug and error logging for troubleshooting

## Directory Structure

```
GithubRepoParser/
├── additional-configs/          # Additional configuration files
│   └── config.ini              # Example additional config
├── constants/                   # Application constants
│   ├── app_constants.py        # Core application constants
│   └── app_message_constants.py # Message and logging constants
├── output/                     # Generated analysis files (auto-created)
│   ├── repo_analysis.txt       # Main analysis report
│   ├── debug.log              # Debug information
│   └── error.log              # Error logs
├── config.ini                  # Default configuration file
├── repo_parser_analyser.py     # Main application script
├── repo_parser_analyser_service.py # Service functions
└── README.md                   # This file
```

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Required Dependencies

Install the required Python packages:

```bash
pip install PyGithub configparser
```

### GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` permissions
3. Save the token securely (you'll need it for authentication)

## Configuration

### 1. Default Configuration File (config.ini)

Create or modify the `config.ini` file in the root directory:

```ini
[github]
repo_owner=pulak-code
repo_name=poc
repo_url=https://github.com/pulak-code/poc
file_to_read=github_repo/build.gradle
build_type=gradle
```

### 2. Additional Configuration Files

Create custom configuration files in the `additional-configs/` directory:

```bash
mkdir -p additional-configs
```

Example `additional-configs/my-project.ini`:
```ini
[github]
repo_owner=myusername
repo_name=myproject
build_type=maven
```

## Usage

### Authentication Options

**Option 1: Command Line Token**
```bash
python repo_parser_analyser.py --token YOUR_GITHUB_TOKEN
```

**Option 2: Environment Variable**
```bash
export GITHUB_TOKEN=your_github_token_here
python repo_parser_analyser.py
```

### Repository Specification Options

#### 1. Using Default Config File

```bash
# Uses config.ini in root directory
python repo_parser_analyser.py --token YOUR_TOKEN
```

#### 2. Using Custom Config File

```bash
# Uses additional-configs/my-project.ini
python repo_parser_analyser.py --token YOUR_TOKEN --config-file my-project
```

#### 3. Using Repository URL

```bash
# Direct GitHub URL specification
python repo_parser_analyser.py --token YOUR_TOKEN --url https://github.com/owner/repo
```

#### 4. Using Owner and Repository Name

```bash
# Specify both owner and repository name
python repo_parser_analyser.py --token YOUR_TOKEN --owner pulak-code --name poc
```

#### 5. Partial Command Line with Config Fallback

```bash
# Specify owner only (repo name from config)
python repo_parser_analyser.py --token YOUR_TOKEN --owner pulak-code

# Specify repo name only (owner from config)
python repo_parser_analyser.py --token YOUR_TOKEN --name my-repo
```

### Build Type Options

```bash
# Specify build type explicitly
python repo_parser_analyser.py --token YOUR_TOKEN --build-type gradle
python repo_parser_analyser.py --token YOUR_TOKEN --build-type maven

# Default is gradle if not specified
python repo_parser_analyser.py --token YOUR_TOKEN
```

### Complete Command Examples

#### Example 1: Basic Usage with Config
```bash
python repo_parser_analyser.py --token ghp_xxxxxxxxxxxxxxxxxxxx
```

#### Example 2: URL with Custom Build Type
```bash
python repo_parser_analyser.py --token ghp_xxxxxxxxxxxxxxxxxxxx --url https://github.com/spring-projects/spring-boot --build-type gradle
```

#### Example 3: Owner/Name with Custom Config
```bash
python repo_parser_analyser.py --token ghp_xxxxxxxxxxxxxxxxxxxx --owner facebook --name react --config-file react-project.ini
```

#### Example 4: Using Environment Variable
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
python repo_parser_analyser.py --owner microsoft --name vscode --build-type gradle
```

#### Example 5: Partial Specification (Owner from command, Name from config)
```bash
python repo_parser_analyser.py --token ghp_xxxxxxxxxxxxxxxxxxxx --owner netflix --config-file netflix-config.ini
```

## Command Line Arguments Reference

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--token` | `-t` | GitHub personal access token | `--token ghp_xxx` |
| `--url` | `-u` | Full GitHub repository URL | `--url https://github.com/owner/repo` |
| `--owner` | `-o` | Repository owner/username | `--owner pulak-code` |
| `--name` | `-n` | Repository name | `--name poc` |
| `--build-type` | `-b` | Build system type | `--build-type gradle` |
| `--config-file` | `-c` | Custom config file name | `--config-file my-project.ini` |

## Output Files

The tool generates three output files in the `output/` directory:

### 1. repo_analysis.txt
Main analysis report containing:
- Repository metadata (name, URL, description, language, stars, forks)
- Complete directory structure
- Build file analysis (if applicable)

### 2. debug.log
Detailed debug information including:
- Connection status
- File reading operations
- Build file parsing details
- Processing steps

### 3. error.log
Error information for troubleshooting:
- API errors
- File access issues
- Configuration problems

## Configuration File Priority

The tool follows this priority order for configuration:

1. **Command line arguments** (highest priority)
2. **Partial command line + config file fallback**
3. **Configuration file values** (lowest priority)

### Priority Examples

```bash
# Basic usage with default config
python repo_parser_analyser.py --token YOUR_TOKEN

# Custom config file
python repo_parser_analyser.py --token YOUR_TOKEN --config-file my-project.ini

# URL specification
python repo_parser_analyser.py --token YOUR_TOKEN --url https://github.com/owner/repo

# Owner and name
python repo_parser_analyser.py --token YOUR_TOKEN --owner pulak-code --name poc

# Partial with fallback
python repo_parser_analyser.py --token YOUR_TOKEN --owner pulak-code
```

## Supported Build Systems

| Build System | File Names | Extension Support |
|--------------|------------|------------------|
| **Gradle** | `build.gradle`, `build.gradle.kts` | Groovy, Kotlin DSL |
| **Maven** | `pom.xml` | XML |

### Build File Analysis Features

**Gradle Files:**
- Project version
- Group ID
- Project name
- Description
- Build number
- Project owner

**Maven Files:**
- Group ID
- Artifact ID
- Version
- Description

## Troubleshooting

### Common Issues

#### 1. Authentication Errors
```
Error: GitHub API Error: 401
```
**Solution:** Check your GitHub token:
- Ensure token has `repo` permissions
- Verify token is not expired
- Check if token is correctly set

#### 2. Repository Not Found
```
Error: GitHub API Error: 404
```
**Solution:** Verify repository details:
- Check repository owner and name spelling
- Ensure repository is public or token has access
- Verify repository URL is correct

#### 3. Config File Not Found
```
Warning: Config file 'custom-config.ini' not found
```
**Solution:** 
- Check if file exists in `additional-configs/` directory
- Verify file name spelling
- Ensure file has `.ini` extension

#### 4. Build File Not Found
```
Warning: No gradle build file found in repository root
```
**Solution:**
- Check if build file exists in repository root
- Try different build type (`--build-type maven`)
- Verify repository contains build files

### Debug Information

Enable detailed logging by checking the `debug.log` file:

```bash
# Run analysis
python repo_parser_analyser.py --token YOUR_TOKEN

# Check debug information
cat output/debug.log

# Check errors
cat output/error.log
```

## Testing the Setup

### Step 1: Test Basic Functionality
```bash
# Test with a public repository
python repo_parser_analyser.py --token YOUR_TOKEN --url https://github.com/octocat/Hello-World
```

### Step 2: Test Config File
```bash
# Test with default config
python repo_parser_analyser.py --token YOUR_TOKEN
```

### Step 3: Test Custom Config
```bash
# Create test config
echo "[github]
repo_owner=microsoft
repo_name=vscode
build_type=gradle" > additional-configs/test-config.ini

# Test custom config
python repo_parser_analyser.py --token YOUR_TOKEN --config-file test-config
```

### Step 4: Verify Output
```bash
# Check if output files are created
ls -la output/

# View analysis report
cat output/repo_analysis.txt
```

## Example Output

### Sample Analysis Report
```
==================================================
REPOSITORY ANALYSIS
==================================================
Repository: pulak-code/poc
URL: https://github.com/pulak-code/poc
Description: Proof of concept repository
Primary Language: Java
Stars: 5 | Forks: 2

==================================================
REPOSITORY STRUCTURE
==================================================
📁 src/
📁 src/main/
📁 src/main/java/
📄 src/main/java/Main.java
📄 build.gradle
📄 README.md

==================================================
BUILD FILE ANALYSIS
==================================================
version: 1.0.0
group: com.example
name: poc-project
description: Sample project
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Support

If you encounter issues:

1. Check the troubleshooting section
2. Review debug logs in `output/debug.log`
3. Check error logs in `output/error.log`
4. Create an issue in the repository with detailed information

---

**Note:** Always keep your GitHub personal access token secure and never commit it to version control.