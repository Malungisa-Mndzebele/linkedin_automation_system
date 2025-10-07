"""
Log Viewer Utility for LinkedIn Job Application Automation
This tool helps analyze and view the detailed logs created by the automation
"""
import os
import re
from datetime import datetime
from typing import List, Dict, Any


class LogAnalyzer:
    """Analyze and display automation logs"""
    
    def __init__(self):
        self.general_log_file = 'linkedin_automation.log'
        self.actions_log_file = 'automation_actions.log'
    
    def check_log_files(self) -> Dict[str, bool]:
        """Check which log files exist"""
        return {
            'general_log': os.path.exists(self.general_log_file),
            'actions_log': os.path.exists(self.actions_log_file)
        }
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Extract session summary from logs"""
        summary = {
            'total_sessions': 0,
            'successful_sessions': 0,
            'failed_sessions': 0,
            'interrupted_sessions': 0,
            'total_applications': 0,
            'last_session_date': None
        }
        
        if not os.path.exists(self.actions_log_file):
            return summary
        
        with open(self.actions_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count session starts
        session_starts = re.findall(r'LINKEDIN AUTOMATION SESSION STARTED', content)
        summary['total_sessions'] = len(session_starts)
        
        # Count successful sessions
        successful_sessions = re.findall(r'LINKEDIN AUTOMATION SESSION COMPLETED SUCCESSFULLY', content)
        summary['successful_sessions'] = len(successful_sessions)
        
        # Count failed sessions
        failed_sessions = re.findall(r'LINKEDIN AUTOMATION SESSION FAILED', content)
        summary['failed_sessions'] = len(failed_sessions)
        
        # Count interrupted sessions
        interrupted_sessions = re.findall(r'LINKEDIN AUTOMATION SESSION INTERRUPTED', content)
        summary['interrupted_sessions'] = len(interrupted_sessions)
        
        # Count total applications
        applications = re.findall(r'SUCCESS - Applied to', content)
        summary['total_applications'] = len(applications)
        
        # Get last session date
        dates = re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', content)
        if dates:
            summary['last_session_date'] = dates[-1]
        
        return summary
    
    def get_recent_applications(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent job applications from logs"""
        applications = []
        
        if not os.path.exists(self.actions_log_file):
            return applications
        
        with open(self.actions_log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Look for application entries
        for line in lines:
            if 'SUCCESS - Applied to' in line or 'FAILED - Could not apply to' in line:
                # Extract timestamp
                timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                timestamp = timestamp_match.group(1) if timestamp_match else 'Unknown'
                
                # Extract job details
                if 'SUCCESS' in line:
                    match = re.search(r"Applied to '([^']+)' at '([^']+)'", line)
                    if match:
                        applications.append({
                            'timestamp': timestamp,
                            'status': 'SUCCESS',
                            'title': match.group(1),
                            'company': match.group(2)
                        })
                elif 'FAILED' in line:
                    match = re.search(r"Could not apply to '([^']+)' at '([^']+)'", line)
                    if match:
                        applications.append({
                            'timestamp': timestamp,
                            'status': 'FAILED',
                            'title': match.group(1),
                            'company': match.group(2)
                        })
        
        # Return most recent applications
        return applications[-limit:] if applications else []
    
    def get_session_statistics(self) -> List[Dict[str, Any]]:
        """Get statistics for each session"""
        sessions = []
        
        if not os.path.exists(self.actions_log_file):
            return sessions
        
        with open(self.actions_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content by session markers
        session_blocks = re.split(r'LINKEDIN AUTOMATION SESSION STARTED', content)
        
        for i, block in enumerate(session_blocks[1:], 1):  # Skip first empty block
            session = {
                'session_number': i,
                'date': None,
                'status': 'UNKNOWN',
                'applications_sent': 0,
                'jobs_found': 0,
                'easy_apply_jobs': 0,
                'success_rate': 0
            }
            
            # Extract date
            date_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', block)
            if date_match:
                session['date'] = date_match.group(1)
            
            # Determine status
            if 'SESSION COMPLETED SUCCESSFULLY' in block:
                session['status'] = 'SUCCESS'
            elif 'SESSION FAILED' in block:
                session['status'] = 'FAILED'
            elif 'SESSION INTERRUPTED' in block:
                session['status'] = 'INTERRUPTED'
            
            # Extract statistics
            apps_match = re.search(r'Total applications sent: (\d+)', block)
            if apps_match:
                session['applications_sent'] = int(apps_match.group(1))
            
            jobs_match = re.search(r'Total jobs found: (\d+)', block)
            if jobs_match:
                session['jobs_found'] = int(jobs_match.group(1))
            
            easy_apply_match = re.search(r'Jobs with Easy Apply: (\d+)', block)
            if easy_apply_match:
                session['easy_apply_jobs'] = int(easy_apply_match.group(1))
            
            success_rate_match = re.search(r'Success rate: ([\d.]+)%', block)
            if success_rate_match:
                session['success_rate'] = float(success_rate_match.group(1))
            
            sessions.append(session)
        
        return sessions
    
    def display_summary(self):
        """Display a summary of all logs"""
        print("=" * 80)
        print("LINKEDIN AUTOMATION LOG SUMMARY")
        print("=" * 80)
        
        # Check log files
        log_files = self.check_log_files()
        print(f"General log file exists: {'Yes' if log_files['general_log'] else 'No'}")
        print(f"Actions log file exists: {'Yes' if log_files['actions_log'] else 'No'}")
        print()
        
        if not log_files['actions_log']:
            print("No action logs found. Run the automation first to generate logs.")
            return
        
        # Get session summary
        summary = self.get_session_summary()
        print("SESSION SUMMARY:")
        print(f"  Total sessions: {summary['total_sessions']}")
        print(f"  Successful sessions: {summary['successful_sessions']}")
        print(f"  Failed sessions: {summary['failed_sessions']}")
        print(f"  Interrupted sessions: {summary['interrupted_sessions']}")
        print(f"  Total applications sent: {summary['total_applications']}")
        print(f"  Last session: {summary['last_session_date'] or 'Never'}")
        print()
        
        # Get recent applications
        recent_apps = self.get_recent_applications(5)
        if recent_apps:
            print("RECENT APPLICATIONS:")
            for app in recent_apps:
                status_icon = "✓" if app['status'] == 'SUCCESS' else "✗"
                print(f"  {status_icon} {app['timestamp']} - {app['title']} at {app['company']}")
            print()
        
        # Get session statistics
        sessions = self.get_session_statistics()
        if sessions:
            print("SESSION STATISTICS:")
            for session in sessions[-3:]:  # Show last 3 sessions
                print(f"  Session {session['session_number']} ({session['date']}):")
                print(f"    Status: {session['status']}")
                print(f"    Applications sent: {session['applications_sent']}")
                print(f"    Jobs found: {session['jobs_found']}")
                print(f"    Easy Apply jobs: {session['easy_apply_jobs']}")
                print(f"    Success rate: {session['success_rate']:.1f}%")
                print()
    
    def display_recent_logs(self, lines: int = 20):
        """Display recent log entries"""
        print("=" * 80)
        print(f"RECENT LOG ENTRIES (Last {lines} lines)")
        print("=" * 80)
        
        if not os.path.exists(self.actions_log_file):
            print("No action logs found.")
            return
        
        with open(self.actions_log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
        
        recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        for line in recent_lines:
            print(line.rstrip())


def main():
    """Main function for log viewer"""
    analyzer = LogAnalyzer()
    
    print("LinkedIn Job Application Automation - Log Viewer")
    print("=" * 60)
    print("1. Display log summary")
    print("2. View recent applications")
    print("3. View session statistics")
    print("4. View recent log entries")
    print("5. Exit")
    print()
    
    while True:
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            analyzer.display_summary()
        elif choice == '2':
            recent_apps = analyzer.get_recent_applications(10)
            if recent_apps:
                print("\nRECENT APPLICATIONS:")
                for app in recent_apps:
                    status_icon = "✓" if app['status'] == 'SUCCESS' else "✗"
                    print(f"  {status_icon} {app['timestamp']} - {app['title']} at {app['company']}")
            else:
                print("No applications found in logs.")
        elif choice == '3':
            sessions = analyzer.get_session_statistics()
            if sessions:
                print("\nSESSION STATISTICS:")
                for session in sessions:
                    print(f"  Session {session['session_number']} ({session['date']}):")
                    print(f"    Status: {session['status']}")
                    print(f"    Applications sent: {session['applications_sent']}")
                    print(f"    Jobs found: {session['jobs_found']}")
                    print(f"    Easy Apply jobs: {session['easy_apply_jobs']}")
                    print(f"    Success rate: {session['success_rate']:.1f}%")
                    print()
            else:
                print("No session data found in logs.")
        elif choice == '4':
            lines = input("Number of lines to display (default 20): ").strip()
            lines = int(lines) if lines.isdigit() else 20
            analyzer.display_recent_logs(lines)
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")
        
        print("\n" + "-" * 60)


if __name__ == "__main__":
    main()
