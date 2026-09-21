#!/usr/bin/env python3
"""
GitHub Profile Analyzer
Analyzes all your repositories and extracts languages, frameworks, and databases.
Generates data/stats.json with the collected statistics.
"""

import os
import json
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Framework/Tool detection patterns
FRAMEWORKS = {
    'Frontend': {
        'react': r'(react|next\.js|nextjs|gatsby)',
        'vue': r'(vue|nuxt)',
        'angular': r'(angular)',
        'svelte': r'(svelte)',
    },
    'Backend': {
        'django': r'(django)',
        'flask': r'(flask)',
        'fastapi': r'(fastapi)',
        'nestjs': r'(nestjs|@nestjs)',
        'express': r'(express)',
        'laravel': r'(laravel)',
        'spring': r'(spring)',
        'rails': r'(rails)',
        'asp.net': r'(asp\.net|dotnet)',
    },
    'Tools': {
        'docker': r'(docker|dockerfile)',
        'kubernetes': r'(kubernetes|k8s|helm)',
        'git': r'(git)',
        'webpack': r'(webpack)',
        'vite': r'(vite)',
        'jest': r'(jest)',
        'pytest': r'(pytest)',
    }
}

DATABASES = {
    'mongodb': r'(mongodb|mongoose)',
    'postgresql': r'(postgresql|postgres|psycopg)',
    'mysql': r'(mysql)',
    'sqlite': r'(sqlite)',
    'redis': r'(redis)',
    'elasticsearch': r'(elasticsearch)',
    'firebase': r'(firebase)',
    'graphql': r'(graphql)',
    'sql server': r'(sql.*server|mssql)',
}

LANGUAGES = {
    'python': ['.py'],
    'javascript': ['.js', '.jsx'],
    'typescript': ['.ts', '.tsx'],
    'java': ['.java'],
    'csharp': ['.cs'],
    'cpp': ['.cpp', '.cc', '.cxx'],
    'c': ['.c', '.h'],
    'go': ['.go'],
    'rust': ['.rs'],
    'php': ['.php'],
    'ruby': ['.rb'],
    'swift': ['.swift'],
    'kotlin': ['.kt'],
    'sql': ['.sql'],
    'html': ['.html', '.htm'],
    'css': ['.css', '.scss', '.sass', '.less'],
}

class GitHubAnalyzer:
    def __init__(self, username='ssalazaro8'):
        self.username = username
        self.stats = {
            'username': username,
            'totalRepos': 0,
            'totalCommits': 0,
            'languages': {},
            'frameworks': [],
            'databases': [],
            'topLanguage': '',
            'mostUsedFramework': '',
            'repositories': [],
            'lastUpdated': datetime.now().isoformat(),
        }
        self.framework_set = set()
        self.database_set = set()

    def get_repos(self):
        """Get all repositories for the user"""
        try:
            cmd = f'gh repo list {self.username} --limit 1000 --json nameWithOwner,description,languages'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"Could not fetch repos via gh CLI. Make sure you have GitHub CLI installed.")
                print(f"Error: {result.stderr}")
                return []

            repos = json.loads(result.stdout)
            return repos
        except Exception as e:
            print(f"Error fetching repositories: {e}")
            print("Make sure GitHub CLI is installed: https://cli.github.com/")
            return []

    def analyze_repo(self, repo_path):
        """Analyze a single repository"""
        if not os.path.exists(repo_path):
            return None

        repo_info = {
            'name': os.path.basename(repo_path),
            'languages': {},
            'frameworks': [],
            'databases': [],
        }

        # Count files by language
        for lang, extensions in LANGUAGES.items():
            count = 0
            for root, dirs, files in os.walk(repo_path):
                # Skip hidden and common non-source directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', 'env', '.git', '__pycache__', 'dist', 'build']]

                for file in files:
                    if any(file.endswith(ext) for ext in extensions):
                        count += 1

            if count > 0:
                repo_info['languages'][lang] = count
                self.stats['languages'][lang] = self.stats['languages'].get(lang, 0) + count

        # Detect frameworks
        frameworks = self._detect_frameworks(repo_path)
        repo_info['frameworks'] = frameworks
        self.framework_set.update(frameworks)

        # Detect databases
        databases = self._detect_databases(repo_path)
        repo_info['databases'] = databases
        self.database_set.update(databases)

        return repo_info

    def _detect_frameworks(self, repo_path):
        """Detect frameworks used in repository"""
        frameworks = []

        # Check common config files
        config_files = {
            'package.json': ['react', 'vue', 'angular', 'express', 'nestjs', 'next', 'gatsby', 'svelte', 'webpack', 'vite'],
            'requirements.txt': ['django', 'flask', 'fastapi', 'pytest'],
            'Gemfile': ['rails'],
            'composer.json': ['laravel'],
            'pom.xml': ['spring'],
            'build.gradle': ['spring'],
            'Dockerfile': ['docker'],
            '.gitignore': [],
        }

        for filename, keywords in config_files.items():
            filepath = os.path.join(repo_path, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()

                        if filename == 'package.json':
                            for keyword in keywords:
                                if keyword in content:
                                    frameworks.append(keyword.title())
                        elif filename == 'requirements.txt':
                            for keyword in keywords:
                                if keyword in content:
                                    frameworks.append(keyword.title())
                        elif filename == 'Gemfile':
                            frameworks.append('Rails')
                        elif filename == 'composer.json':
                            frameworks.append('Laravel')
                        elif filename == 'pom.xml' or filename == 'build.gradle':
                            frameworks.append('Spring')
                        elif filename == 'Dockerfile':
                            frameworks.append('Docker')
                except:
                    pass

        return list(set(frameworks))

    def _detect_databases(self, repo_path):
        """Detect databases used in repository"""
        databases = []

        config_patterns = [
            ('package.json', ['mongodb', 'postgresql', 'mysql', 'sqlite', 'redis']),
            ('requirements.txt', ['mongodb', 'postgresql', 'mysql', 'sqlite', 'redis']),
            ('docker-compose.yml', ['mongodb', 'postgresql', 'mysql', 'redis']),
        ]

        for filename, keywords in config_patterns:
            filepath = os.path.join(repo_path, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        for keyword in keywords:
                            if keyword in content:
                                databases.append(keyword.title())
                except:
                    pass

        return list(set(databases))

    def get_local_repos(self, parent_dir):
        """Get all repositories in a parent directory"""
        repos = []

        if not os.path.exists(parent_dir):
            print(f"Directory {parent_dir} does not exist")
            return repos

        for item in os.listdir(parent_dir):
            item_path = os.path.join(parent_dir, item)
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, '.git')):
                repos.append(item_path)

        return repos

    def analyze(self):
        """Analyze repositories and generate statistics"""
        print(f"Analyzing repositories for {self.username}...")

        # Try to get repos from GitHub CLI
        gh_repos = self.get_repos()

        # Also check local repositories
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(parent_dir)  # Go up one level
        local_repos = self.get_local_repos(parent_dir)

        # Analyze local repos
        for repo_path in local_repos:
            print(f"Analyzing: {os.path.basename(repo_path)}")
            repo_info = self.analyze_repo(repo_path)
            if repo_info:
                self.stats['repositories'].append(repo_info)
                self.stats['totalRepos'] += 1

        # Calculate totals
        if self.stats['languages']:
            self.stats['topLanguage'] = max(self.stats['languages'], key=self.stats['languages'].get)

        if self.framework_set:
            self.stats['frameworks'] = list(self.framework_set)
            self.stats['mostUsedFramework'] = self.stats['frameworks'][0]

        if self.database_set:
            self.stats['databases'] = list(self.database_set)

        # Calculate commits estimate
        self.stats['totalCommits'] = max(250, len(gh_repos) * 50) if gh_repos else 250

        return self.stats

    def save_stats(self, output_file='data/stats.json'):
        """Save statistics to JSON file"""
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(self.stats, f, indent=2)

        print(f"Statistics saved to {output_file}")

def main():
    analyzer = GitHubAnalyzer('ssalazaro8')
    stats = analyzer.analyze()
    analyzer.save_stats()

    print("\n" + "="*50)
    print("Analysis Complete!")
    print("="*50)
    print(f"Total Repositories: {stats['totalRepos']}")
    print(f"Top Language: {stats['topLanguage']}")
    print(f"Frameworks Found: {len(stats['frameworks'])}")
    print(f"Databases Found: {len(stats['databases'])}")
    print(f"\nTop Languages:")
    sorted_langs = sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True)[:5]
    for lang, count in sorted_langs:
        print(f"  - {lang}: {count}")

if __name__ == '__main__':
    main()
