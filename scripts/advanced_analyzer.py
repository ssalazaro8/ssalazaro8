#!/usr/bin/env python3
"""
Advanced GitHub Profile Analyzer
Fetches and analyzes ALL repositories from GitHub using the GitHub API.
Generates comprehensive statistics and visual metrics.
"""

import os
import json
import subprocess
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import re

class AdvancedGitHubAnalyzer:
    def __init__(self, username='ssalazaro8'):
        self.username = username
        self.stats = {
            'username': username,
            'totalRepos': 0,
            'totalCommits': 0,
            'totalStars': 0,
            'languages': {},
            'frameworks': [],
            'databases': [],
            'topLanguages': [],
            'projectsByLanguage': {},
            'languagesByProject': {},
            'repositories': [],
            'lastUpdated': datetime.now().isoformat(),
        }
        self.framework_counter = Counter()
        self.database_counter = Counter()
        self.language_counter = Counter()

    def fetch_repos_via_cli(self):
        """Fetch repositories using GitHub CLI with detailed info"""
        try:
            # Get repo list with additional fields
            cmd = f'gh repo list {self.username} --limit 100 --json nameWithOwner,name,description,languages,stargazerCount,forkCount,primaryLanguage,url'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"Error fetching repos via gh CLI")
                return []

            repos = json.loads(result.stdout)
            return repos
        except Exception as e:
            print(f"Error: {e}")
            return []

    def analyze_repo_content(self, repo_name):
        """Analyze repository content for frameworks and databases"""
        frameworks = set()
        databases = set()

        try:
            # Get file list from the repo
            cmd = f'gh repo view {self.username}/{repo_name} --json name,description,url'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            # Try to get README or package.json content
            readme_cmd = f'gh api repos/{self.username}/{repo_name}/readme --template="{{{{.content}}}}"'
            readme_result = subprocess.run(readme_cmd, shell=True, capture_output=True, text=True)

            content = readme_result.stdout.lower() + result.stdout.lower()

            # Detect frameworks
            framework_patterns = {
                'react': r'\breact\b|next\.js|nextjs',
                'angular': r'\bangular\b',
                'vue': r'\bvue\b|nuxt',
                'django': r'\bdjango\b',
                'flask': r'\bflask\b',
                'fastapi': r'\bfastapi\b|fast api',
                'nestjs': r'\bnestjs\b|nest\.js',
                'express': r'\bexpress\b|expressjs',
                'laravel': r'\blaravel\b',
                'spring': r'\bspring\b|spring boot',
                'asp.net': r'\basp\.net\b|asp net|dotnet',
                'rails': r'\brails\b|ruby on rails',
                'svelte': r'\bsvelte\b',
                'gatsby': r'\bgatsby\b',
            }

            for fw, pattern in framework_patterns.items():
                if re.search(pattern, content):
                    frameworks.add(fw.title())

            # Detect databases
            database_patterns = {
                'mongodb': r'\bmongodb\b|mongo\b',
                'postgresql': r'\bpostgres\b|postgresql\b',
                'mysql': r'\bmysql\b',
                'sqlite': r'\bsqlite\b',
                'redis': r'\bredis\b',
                'firebase': r'\bfirebase\b',
                'graphql': r'\bgraphql\b',
                'sql server': r'\bsql server\b|mssql\b',
                'elasticsearch': r'\belasticsearch\b',
                'dynamodb': r'\bdynamodb\b',
            }

            for db, pattern in database_patterns.items():
                if re.search(pattern, content):
                    databases.add(db.title())

        except Exception as e:
            pass

        return list(frameworks), list(databases)

    def analyze(self):
        """Analyze all repositories"""
        print(f"🔍 Analyzing {len(self.repos)} repositories for {self.username}...")

        for repo in self.repos:
            repo_name = repo.get('name', '')
            repo_url = repo.get('url', '')
            primary_lang = repo.get('primaryLanguage')
            languages = repo.get('languages', [])
            stars = repo.get('stargazerCount', 0)

            print(f"  📦 {repo_name}")

            # Count languages
            if languages:
                for lang in languages:
                    self.language_counter[lang] += 1
                    if lang not in self.stats['languages']:
                        self.stats['languages'][lang] = 0
                    self.stats['languages'][lang] += 1

            # Analyze for frameworks and databases
            frameworks, databases = self.analyze_repo_content(repo_name)

            for fw in frameworks:
                self.framework_counter[fw] += 1

            for db in databases:
                self.database_counter[db] += 1

            # Store repository info
            repo_info = {
                'name': repo_name,
                'url': repo_url,
                'languages': languages,
                'frameworks': frameworks,
                'databases': databases,
                'stars': stars,
                'primaryLanguage': primary_lang,
            }

            self.stats['repositories'].append(repo_info)
            self.stats['totalRepos'] += 1
            self.stats['totalStars'] += stars

            # Group by language
            if primary_lang:
                if primary_lang not in self.stats['projectsByLanguage']:
                    self.stats['projectsByLanguage'][primary_lang] = []
                self.stats['projectsByLanguage'][primary_lang].append(repo_name)

        # Sort and compile final statistics
        self.stats['topLanguages'] = [
            {'name': lang, 'count': count}
            for lang, count in self.language_counter.most_common(10)
        ]

        self.stats['frameworks'] = [
            fw for fw, _ in self.framework_counter.most_common(15)
        ]

        self.stats['databases'] = [
            db for db, _ in self.database_counter.most_common(10)
        ]

        # Set top stats
        if self.stats['topLanguages']:
            self.stats['topLanguage'] = self.stats['topLanguages'][0]['name']

        if self.stats['frameworks']:
            self.stats['mostUsedFramework'] = self.stats['frameworks'][0]

        # Estimate commits
        self.stats['totalCommits'] = self.stats['totalRepos'] * 50

        print(f"\n✅ Analysis complete!")
        print(f"   📊 Total Repos: {self.stats['totalRepos']}")
        print(f"   ⭐ Total Stars: {self.stats['totalStars']}")
        print(f"   🗣️ Languages: {len(self.stats['languages'])}")
        print(f"   🔧 Frameworks: {len(self.stats['frameworks'])}")

        return self.stats

    def fetch_and_analyze(self):
        """Main method to fetch and analyze"""
        print(f"\n🚀 Starting Advanced GitHub Analysis for @{self.username}\n")

        self.repos = self.fetch_repos_via_cli()

        if not self.repos:
            print("❌ No repositories found or GitHub CLI not authenticated")
            print("💡 Make sure to run: gh auth login")
            return None

        print(f"✓ Found {len(self.repos)} repositories\n")

        return self.analyze()

    def save_stats(self, output_file='data/stats.json'):
        """Save statistics to JSON file"""
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(self.stats, f, indent=2)

        print(f"\n💾 Statistics saved to {output_file}")

    def generate_markdown_report(self, output_file='PROFILE_METRICS.md'):
        """Generate a markdown report with all metrics"""

        md = f"""# 📊 {self.username} - GitHub Profile Metrics

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## 📈 Overview

| Metric | Value |
|--------|-------|
| Total Repositories | {self.stats['totalRepos']} |
| Total Stars | ⭐ {self.stats['totalStars']} |
| Total Commits (est.) | {self.stats['totalCommits']} |
| Languages Used | {len(self.stats['languages'])} |
| Frameworks | {len(self.stats['frameworks'])} |
| Databases | {len(self.stats['databases'])} |
| Top Language | {self.stats['topLanguage']} |

---

## 🗣️ Language Distribution

### Top 10 Languages by Usage
"""

        for i, lang_info in enumerate(self.stats['topLanguages'], 1):
            lang = lang_info['name']
            count = lang_info['count']
            percentage = (count / self.stats['totalRepos']) * 100
            bar_length = int(percentage / 5)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            md += f"\n{i}. **{lang}** ({count} repos - {percentage:.1f}%)\n   `{bar}`"

        md += "\n\n---\n\n## 🔧 Frameworks Used\n\n"

        if self.stats['frameworks']:
            for fw in self.stats['frameworks'][:15]:
                md += f"- {fw}\n"

        md += "\n---\n\n## 🗄️ Databases\n\n"

        if self.stats['databases']:
            for db in self.stats['databases'][:10]:
                md += f"- {db}\n"

        md += "\n---\n\n## 📦 Projects by Primary Language\n\n"

        for lang, projects in sorted(self.stats['projectsByLanguage'].items(),
                                      key=lambda x: len(x[1]), reverse=True):
            md += f"\n### {lang} ({len(projects)} projects)\n\n"
            for project in projects[:10]:
                md += f"- `{project}`\n"
            if len(projects) > 10:
                md += f"- ... and {len(projects) - 10} more\n"

        md += "\n---\n\n## 🎯 Repository Details\n\n"

        # Sort by stars
        sorted_repos = sorted(self.stats['repositories'],
                             key=lambda x: x['stars'], reverse=True)

        for repo in sorted_repos[:20]:
            md += f"\n### ⭐ {repo['name']} ({repo['stars']} stars)\n"
            if repo['primaryLanguage']:
                md += f"- **Primary Language:** {repo['primaryLanguage']}\n"
            if repo['languages']:
                md += f"- **Languages:** {', '.join(repo['languages'][:5])}\n"
            if repo['frameworks']:
                md += f"- **Frameworks:** {', '.join(repo['frameworks'])}\n"
            if repo['databases']:
                md += f"- **Databases:** {', '.join(repo['databases'])}\n"

        # Save markdown
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(md)

        print(f"📄 Markdown report saved to {output_file}")

def main():
    analyzer = AdvancedGitHubAnalyzer('ssalazaro8')
    stats = analyzer.fetch_and_analyze()

    if stats:
        analyzer.save_stats()
        analyzer.generate_markdown_report()

        print("\n" + "="*60)
        print("✨ Analysis Complete!")
        print("="*60)
        print(f"\n📊 Files generated:")
        print(f"   - data/stats.json (for dashboard)")
        print(f"   - PROFILE_METRICS.md (detailed report)")

if __name__ == '__main__':
    main()
