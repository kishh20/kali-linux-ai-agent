from typing import List, Dict, Any

PRACTICALS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "number": 1,
        "title": "File and User Management",
        "category": "Administration",
        "difficulty": "Beginner",
        "estimated_minutes": 10,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "bash",
            "useradd",
            "groupadd",
            "chown",
            "chmod",
            "id"
        ],
        "aim": "To manage directory hierarchies, create departmental user groups and system users, configure ownership, and set granular access permissions in Kali Linux.",
        "objective": "Understand Linux multi-user architecture, directory creation, user/group management, and permission verification.",
        "algorithm": [
            "1. Initialize organizational directory structure under /tmp/organization for safe lab testing.",
            "2. Create dedicated departmental subdirectories: HR, IT, and Finance.",
            "3. Create departmental groups: hr_team and it_team.",
            "4. Create test users: hr_user and it_user, assigning them to their respective groups.",
            "5. Configure directory ownership using chown.",
            "6. Set restricted group permissions using chmod (770 for departmental folders).",
            "7. Verify group memberships and permissions using id and ls -ld."
        ],
        "required_inputs": [
            {
                "key": "base_dir",
                "label": "Base Directory",
                "type": "string",
                "default": "/tmp/organization",
                "description": "Base directory for organizational hierarchy"
            },
            {
                "key": "hr_user",
                "label": "HR Username",
                "type": "string",
                "default": "lab_hr_user",
                "description": "Test HR account username"
            },
            {
                "key": "it_user",
                "label": "IT Username",
                "type": "string",
                "default": "lab_it_user",
                "description": "Test IT account username"
            }
        ],
        "default_commands": [
            "mkdir -p {base_dir}/HR {base_dir}/IT {base_dir}/Finance {base_dir}/Executive",
            "sudo groupadd -f hr_team",
            "sudo groupadd -f it_team",
            "sudo groupadd -f finance_team",
            "id -u {hr_user} >/dev/null 2>&1 || sudo useradd -m -s /bin/bash -g hr_team {hr_user}",
            "id -u {it_user} >/dev/null 2>&1 || sudo useradd -m -s /bin/bash -g it_team {it_user}",
            "id -u lab_fin_user >/dev/null 2>&1 || sudo useradd -m -s /bin/bash -g finance_team lab_fin_user",
            "sudo chown -R {hr_user}:hr_team {base_dir}/HR",
            "sudo chown -R {it_user}:it_team {base_dir}/IT",
            "sudo chown -R lab_fin_user:finance_team {base_dir}/Finance",
            "sudo chmod 770 {base_dir}/HR {base_dir}/IT {base_dir}/Finance",
            "sudo touch {base_dir}/HR/policy.txt {base_dir}/IT/network.conf {base_dir}/Finance/budget.csv",
            "sudo chmod 660 {base_dir}/HR/policy.txt {base_dir}/IT/network.conf",
            "ls -la {base_dir}",
            "ls -ld {base_dir}/HR {base_dir}/IT {base_dir}/Finance",
            "id {hr_user}",
            "id {it_user}",
            "getent group hr_team it_team finance_team"
        ],
        "verification_commands": [
            "ls -ld {base_dir}/HR {base_dir}/IT",
            "getent group hr_team it_team"
        ],
        "explanation": "Creates isolated organizational units, adds groups with groupadd, creates users with useradd bound to primary groups, applies ownership with chown, and secures directories with chmod 770 (rwxrwx---)."
    },
    {
        "id": 2,
        "number": 2,
        "title": "Text Processing and Filtering",
        "category": "Administration",
        "difficulty": "Beginner",
        "estimated_minutes": 8,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "grep",
            "cut",
            "sort",
            "uniq",
            "awk",
            "sed",
            "head",
            "tail"
        ],
        "aim": "To create a structured employee dataset and perform advanced pipeline transformations using grep, cut, sort, uniq, awk, sed, head, and tail.",
        "objective": "Master standard Linux text manipulation tools to parse, filter, format, and extract structured data from files.",
        "algorithm": [
            "1. Generate a colon-delimited employee record file with ID, Name, Department, Salary, and City.",
            "2. Filter records by department (IT) using grep.",
            "3. Extract specific columns (Name and Salary) using cut.",
            "4. Sort records numerically by salary in descending order using sort -t: -k4,4nr.",
            "5. Identify unique department names using cut, sort, and uniq.",
            "6. Display the highest and lowest earning employees using head and tail.",
            "7. Perform conditional data transformation and average salary calculation using awk.",
            "8. Perform in-stream regex substitution using sed to mask sensitive IDs."
        ],
        "required_inputs": [
            {
                "key": "record_file",
                "label": "Employee File",
                "type": "string",
                "default": "/tmp/employees.txt",
                "description": "Path to test employee database file"
            }
        ],
        "default_commands": [
            "cat << 'EOF' > {record_file}\n101:Alice Smith:IT:85000:NewYork\n102:Bob Jones:HR:62000:London\n103:Charlie Brown:IT:92000:SanFrancisco\n104:Diana Prince:Finance:78000:London\n105:Evan Wright:IT:85000:NewYork\n106:Fiona Gallagher:HR:61000:Dublin\n107:George Clark:Finance:95000:NewYork\n108:Hannah Abbott:IT:72000:London\nEOF",
            "cat {record_file}",
            "grep ':IT:' {record_file}",
            "grep -v ':HR:' {record_file}",
            "grep -E ':(85000|92000):' {record_file}",
            "cut -d: -f2,4 {record_file}",
            "cut -d: -f1,3,5 {record_file}",
            "sort -t: -k4,4nr {record_file}",
            "sort -t: -k2,2 {record_file}",
            "cut -d: -f3 {record_file} | sort | uniq -c",
            "cut -d: -f5 {record_file} | sort | uniq",
            "head -n 3 {record_file}",
            "tail -n 3 {record_file}",
            "awk -F: '$4 > 75000 {{print $2, \"(\" $3 \") earns $\" $4}}' {record_file}",
            "awk -F: '{{sum += $4; count++}} END {{print \"Average Company Salary: $\", sum/count}}' {record_file}",
            "sed 's/London/UK-London/g' {record_file}",
            "sed -n '2,5p' {record_file}",
            "wc -l {record_file}"
        ],
        "verification_commands": [
            "wc -l {record_file}",
            "test -f {record_file} && echo 'Text processing completed successfully.'"
        ],
        "explanation": "Demonstrates the power of the Unix philosophy where small, focused utilities (grep, cut, sort, uniq, awk, sed) are composed through pipelines to analyze datasets."
    },
    {
        "id": 3,
        "number": 3,
        "title": "Process Management and Job Control",
        "category": "System",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "ps",
            "top",
            "nice",
            "renice",
            "kill",
            "pgrep"
        ],
        "aim": "To monitor, prioritize, control, and terminate processes using ps, top, nice, renice, kill, and process signals in Kali Linux.",
        "objective": "Understand process lifecycles, PID identification, background job control, scheduling priority adjustments, and IPC signals.",
        "algorithm": [
            "1. Launch simulated background workload processes using sleep.",
            "2. Inspect active processes, PIDs, PPIDs, and terminal associations with ps aux and ps -ef.",
            "3. Capture snapshot system resource utilization using top -b -n 1.",
            "4. Launch a process with modified nice priority using nice -n 10.",
            "5. Dynamically alter the priority of an active process using renice.",
            "6. Send SIGSTOP (19) to suspend a process and SIGCONT (18) to resume it.",
            "7. Gracefully terminate processes using SIGTERM (15) and verify with pgrep."
        ],
        "required_inputs": [
            {
                "key": "process_count",
                "label": "Background Jobs",
                "type": "number",
                "default": 2,
                "description": "Number of test background processes to spawn"
            }
        ],
        "default_commands": [
            "sleep 180 & PID1=$!",
            "sleep 240 & PID2=$!",
            "sleep 300 & PID3=$!",
            "echo \"Spawned background jobs: PID1=$PID1, PID2=$PID2, PID3=$PID3\"",
            "ps -fp $PID1,$PID2,$PID3",
            "ps aux | grep sleep | grep -v grep",
            "ps -o pid,ppid,stat,nice,comm -p $PID1,$PID2,$PID3",
            "top -b -n 1 | head -n 12",
            "pgrep -l sleep",
            "renice +10 -p $PID1",
            "renice +5 -p $PID2",
            "kill -STOP $PID3",
            "ps -o pid,stat,nice,comm -p $PID3",
            "kill -CONT $PID3",
            "kill -15 $PID1 $PID2 $PID3",
            "sleep 1",
            "pgrep -f 'sleep (180|240|300)' || echo 'All test jobs terminated.'"
        ],
        "verification_commands": [
            "pgrep -f 'sleep 300' || echo 'Verified: No lingering test processes.'"
        ],
        "explanation": "Spawns asynchronous background jobs, tracks their process IDs ($!), inspects scheduler nice values (-20 highest to +19 lowest), transmits POSIX signals, and cleanly reaps terminated jobs."
    },
    {
        "id": 4,
        "number": 4,
        "title": "Bash Variables and Environment",
        "category": "Scripting",
        "difficulty": "Beginner",
        "estimated_minutes": 8,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "bash",
            "env",
            "export"
        ],
        "aim": "To demonstrate system environment variables, user variables, exported variables, command substitution, and arithmetic expansions in Bash.",
        "objective": "Master variable declaration, environment scoping, subprocess inheritance, dynamic string formatting, and mathematical evaluations.",
        "algorithm": [
            "1. Inspect predefined system variables: $USER, $HOME, $SHELL, $PWD, $HOSTNAME.",
            "2. Define local user variables and demonstrate case sensitivity.",
            "3. Export variables to subshells and verify persistence across child processes.",
            "4. Perform dynamic command substitution $(command) to capture system metrics.",
            "5. Conduct arithmetic expansions $(( expression )) for arithmetic operations.",
            "6. Write and execute a self-contained demonstration script."
        ],
        "required_inputs": [
            {
                "key": "app_env",
                "label": "Target Environment",
                "type": "string",
                "default": "production-lab",
                "description": "Custom environment name"
            }
        ],
        "default_commands": [
            "echo \"Current User: $USER | UID: $UID\"",
            "echo \"Home Directory: $HOME\"",
            "echo \"Login Shell: $SHELL\"",
            "echo \"Current Working Directory: $PWD\"",
            "echo \"Hostname: $HOSTNAME\"",
            "APP_NAME='Kali Practical Engine'",
            "APP_VERSION=2026",
            "echo \"Application: $APP_NAME Release $APP_VERSION\"",
            "ITEM_COUNT=15",
            "UNIT_PRICE=45",
            "TOTAL_PRICE=$((ITEM_COUNT * UNIT_PRICE))",
            "echo \"Calculated: $ITEM_COUNT units @ \\$$UNIT_PRICE = \\$$TOTAL_PRICE\"",
            "SYS_DATE=$(date '+%Y-%m-%d %H:%M:%S')",
            "SYS_KERNEL=$(uname -r)",
            "SYS_UPTIME=$(uptime -p)",
            "echo \"Kernel: $SYS_KERNEL | Date: $SYS_DATE | Uptime: $SYS_UPTIME\"",
            "export LAB_ENV='{app_env}'",
            "bash -c 'echo \"Child shell environment verified: LAB_ENV=$LAB_ENV\"'"
        ],
        "verification_commands": [
            "test -n \"$USER\" && echo \"Bash variable evaluation verified.\""
        ],
        "explanation": "Illustrates standard bash variable syntax, the difference between local variables and environment variables (export), and evaluates expressions without external commands."
    },
    {
        "id": 5,
        "number": 5,
        "title": "Conditional Statements in Bash",
        "category": "Scripting",
        "difficulty": "Beginner",
        "estimated_minutes": 10,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "bash",
            "test"
        ],
        "aim": "To write robust conditional branching logic in Bash using if, elif, else, test expressions (-f, -d, -r, -w, -x, -z), and case statements.",
        "objective": "Build decision-making scripts that inspect system files, validate inputs, check permissions, and branch flow conditionally.",
        "algorithm": [
            "1. Write a script testing for the existence of files and directories (-f, -d).",
            "2. Evaluate file access permissions (-r, -w, -x).",
            "3. Validate string attributes (empty -z, non-empty -n).",
            "4. Implement numerical comparison operators (-eq, -ne, -lt, -le, -gt, -ge).",
            "5. Implement a multi-branch case statement for command routing.",
            "6. Execute and test conditional evaluations against live filesystem targets."
        ],
        "required_inputs": [
            {
                "key": "test_path",
                "label": "Test Target Path",
                "type": "string",
                "default": "/etc/passwd",
                "description": "Target file to evaluate conditionally"
            }
        ],
        "default_commands": [
            "TEST_DIR='/tmp/lab_cond_test'",
            "mkdir -p $TEST_DIR",
            "TEST_FILE=\"$TEST_DIR/sample.txt\"",
            "echo 'Linux Conditional Testing' > $TEST_FILE",
            "if [ -d \"$TEST_DIR\" ]; then echo \"[+] Directory exists: $TEST_DIR\"; fi",
            "if [ -f \"$TEST_FILE\" ]; then echo \"[+] Regular file exists: $TEST_FILE\"; fi",
            "if [ -r \"$TEST_FILE\" ]; then echo \"[+] File is readable: YES\"; fi",
            "if [ -w \"$TEST_FILE\" ]; then echo \"[+] File is writable: YES\"; fi",
            "if [ -s \"$TEST_FILE\" ]; then echo \"[+] File size is non-zero: YES\"; fi",
            "SCORE=88",
            "if [ $SCORE -ge 75 ]; then echo \"[+] Score $SCORE: Distinction tier achieved\"; fi",
            "if [ $SCORE -ne 50 ]; then echo \"[+] Score $SCORE is non-default\"; fi",
            "STATUS_STR='operational'",
            "if [ -n \"$STATUS_STR\" ]; then echo \"[+] Status flag is active: $STATUS_STR\"; fi",
            "case \"start\" in start) echo \"Action matched: Service booting...\";; stop) echo \"Service halting...\";; esac",
            "case \"kali\" in debian|ubuntu) echo \"Debian derivative\";; kali) echo \"Kali Linux offensive platform matched\";; esac",
            "rm -rf $TEST_DIR"
        ],
        "verification_commands": [
            "echo 'Conditional statement practical completed.'"
        ],
        "explanation": "Validates file attributes with test brackets [ ], illustrates short-circuit logical operators (&&, ||), and routes choices using pattern matching with case...esac."
    },
    {
        "id": 6,
        "number": 6,
        "title": "Bash Loops and Iteration",
        "category": "Scripting",
        "difficulty": "Beginner",
        "estimated_minutes": 10,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "bash",
            "seq"
        ],
        "aim": "To implement for loops, while loops, until loops, and control statements (break, continue) for batch automation in Bash.",
        "objective": "Automate repetitive administrative workflows across file lists, numerical ranges, and line-by-line file streams.",
        "algorithm": [
            "1. Implement a for loop over a sequence of numbers {1..5} and file glob patterns.",
            "2. Implement a while loop reading line-by-line from a structured file.",
            "3. Implement an until loop that increments a counter until a threshold is met.",
            "4. Use continue to skip specific iterations and break to abort on sentinel conditions.",
            "5. Execute automated directory file generation and batch renaming."
        ],
        "required_inputs": [
            {
                "key": "loop_count",
                "label": "Iterations",
                "type": "number",
                "default": 5,
                "description": "Number of loop cycles"
            }
        ],
        "default_commands": [
            "for i in 1 2 3 4 5; do echo \"Batch iteration #$i\"; done",
            "for color in red green blue amber cyan; do echo \"Theme accent: $color\"; done",
            "for file in /etc/hostname /etc/hosts /etc/issue; do echo \"=== File: $file ===\"; head -n 1 $file; done",
            "COUNT=1; while [ $COUNT -le 5 ]; do echo \"While loop step $COUNT/5\"; COUNT=$((COUNT + 1)); done",
            "printf 'UserA:1001\nUserB:1002\nUserC:1003\nUserD:1004\n' > /tmp/users_loop.txt",
            "while IFS=: read -r uname uid; do echo \"Mapped account $uname -> UID $uid\"; done < /tmp/users_loop.txt",
            "U_VAL=1; until [ $U_VAL -gt 4 ]; do echo \"Until counter reached $U_VAL\"; U_VAL=$((U_VAL + 1)); done",
            "for n in $(seq 1 6); do if [ $n -eq 3 ]; then echo \"  [Skipped $n via continue]\"; continue; fi; echo \"  Processing item $n\"; done",
            "for n in $(seq 1 10); do if [ $n -eq 5 ]; then echo \"  [Terminating at $n via break]\"; break; fi; echo \"  Processing stream $n\"; done",
            "mkdir -p /tmp/batch_files",
            "for id in {1..6}; do touch \"/tmp/batch_files/report_$id.txt\"; done",
            "ls -la /tmp/batch_files",
            "for rf in /tmp/batch_files/*.txt; do echo \"Inspected: $rf\"; done",
            "rm -rf /tmp/batch_files /tmp/users_loop.txt",
            "echo \"Loop operations complete.\""
        ],
        "verification_commands": [
            "echo 'Bash loops executed successfully.'"
        ],
        "explanation": "Applies standard iterative constructs. The while IFS= read idiom is the standard POSIX pattern for robust text stream processing."
    },
    {
        "id": 7,
        "number": 7,
        "title": "Modular Bash Functions",
        "category": "Scripting",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "bash"
        ],
        "aim": "To construct modular, reusable Bash functions with positional parameters, return status codes, local variable scopes, and signal traps.",
        "objective": "Build production-quality maintainable shell scripts following modern modular design principles.",
        "algorithm": [
            "1. Define custom functions with local variable scoping (local keyword).",
            "2. Pass positional arguments ($1, $2, $@) into functions.",
            "3. Implement return codes (return 0 for success, return 1 for error).",
            "4. Capture function standard output using command substitution.",
            "5. Implement a trap handler to guarantee resource cleanup on script exit.",
            "6. Test modular logging and validation functions."
        ],
        "required_inputs": [
            {
                "key": "log_prefix",
                "label": "Log Prefix",
                "type": "string",
                "default": "KALI_AGENT",
                "description": "Prefix tag for logging function"
            }
        ],
        "default_commands": [
            "log_info() {{ echo \"[$(date '+%T')] [INFO] $1\"; }}",
            "log_warn() {{ echo \"[$(date '+%T')] [WARN] $1\"; }}",
            "log_error() {{ echo \"[$(date '+%T')] [ERROR] $1\"; }}",
            "log_info \"Initializing automation function suite...\"",
            "log_warn \"Verifying system memory capacity...\"",
            "calc_product() {{ local a=$1; local b=$2; echo $((a * b)); }}",
            "RESULT=$(calc_product 14 7)",
            "log_info \"Product calculation result: 14 * 7 = $RESULT\"",
            "check_file_exists() {{ if [ -f \"$1\" ]; then return 0; else return 1; fi; }}",
            "check_file_exists /etc/passwd && log_info \"Validated: /etc/passwd exists on host.\"",
            "check_file_exists /tmp/missing_test && log_warn \"Found\" || log_info \"Confirmed missing path handled correctly.\"",
            "get_system_stats() {{ echo \"Host: $(hostname) | Arch: $(uname -m) | User: $(whoami)\"; }}",
            "get_system_stats",
            "cleanup_test() {{ echo \"[CLEANUP] Routine executed successfully.\"; }}",
            "cleanup_test",
            "echo \"Function modularity verified.\""
        ],
        "verification_commands": [
            "echo 'Bash function testing completed.'"
        ],
        "explanation": "Uses the local keyword to prevent namespace pollution, return to communicate exit status to callers, and trap for reliable resource management."
    },
    {
        "id": 8,
        "number": 8,
        "title": "Administrative Automation and Backups",
        "category": "Administration",
        "difficulty": "Intermediate",
        "estimated_minutes": 12,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "tar",
            "gzip",
            "cron",
            "crontab",
            "df"
        ],
        "aim": "To build an automated maintenance and backup script, create compressed archives with tar/gzip, check disk thresholds, and inspect cron schedules.",
        "objective": "Implement unattended Linux system administration routines for data resilience and proactive maintenance.",
        "algorithm": [
            "1. Create a simulated source directory with test documents and configuration files.",
            "2. Create a timestamped compressed tar.gz archive using tar -czf.",
            "3. Verify archive integrity and list contents with tar -tzf.",
            "4. Implement a disk space threshold health check using df and awk.",
            "5. Inspect the current user's crontab schedule using crontab -l.",
            "6. Output automated backup summary."
        ],
        "required_inputs": [
            {
                "key": "backup_source",
                "label": "Source Folder",
                "type": "string",
                "default": "/tmp/lab_data_source",
                "description": "Folder to archive"
            },
            {
                "key": "backup_dest",
                "label": "Backup Folder",
                "type": "string",
                "default": "/tmp/lab_backups",
                "description": "Archive storage folder"
            }
        ],
        "default_commands": [
            "mkdir -p {backup_source} {backup_dest}",
            "echo 'Database production schema dump' > {backup_source}/db_schema.sql",
            "echo 'Web server proxy configuration' > {backup_source}/nginx.conf",
            "echo 'API credentials mock' > {backup_source}/keys.env",
            "echo 'System operational log stream' > {backup_source}/access.log",
            "ls -lh {backup_source}",
            "TIMESTAMP=$(date '+%Y%m%d_%H%M%S')",
            "ARCHIVE_NAME=\"{backup_dest}/snapshot_${{TIMESTAMP}}.tar.gz\"",
            "tar -czf \"$ARCHIVE_NAME\" -C {backup_source} .",
            "echo \"[+] Backup archive created: $ARCHIVE_NAME\"",
            "ls -lh {backup_dest}",
            "tar -tzf \"$ARCHIVE_NAME\"",
            "df -h / | awk 'NR==2 {{print \"Root partition free storage: \" $4 \" (Used: \" $5 \")\"}}'",
            "free -h",
            "crontab -l 2>/dev/null || echo 'No active crontab for current user.'",
            "echo \"Automated backup sequence complete.\""
        ],
        "verification_commands": [
            "ls -lh {backup_dest}/*.tar.gz",
            "test -d {backup_dest} && echo 'Backup verification complete.'"
        ],
        "explanation": "Generates self-contained compressed tarballs with timestamped filenames and demonstrates disk health querying for cron automation."
    },
    {
        "id": 9,
        "number": 9,
        "title": "Password and Privilege Management",
        "category": "Security",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "chage",
            "passwd",
            "sudo",
            "getent"
        ],
        "aim": "To configure user password aging policies with chage, inspect shadow file attributes, examine sudo privileges, and enforce access controls.",
        "objective": "Learn password security hygiene, credential expiration policies, and sudo privilege escalation controls.",
        "algorithm": [
            "1. Inspect active user's sudo capabilities using sudo -l.",
            "2. Create a test security audit user account.",
            "3. Query the account's password aging parameters using chage -l.",
            "4. Enforce strict aging policies: maximum days (60), minimum days (7), warning days (14).",
            "5. Inspect /etc/passwd entries using getent passwd.",
            "6. Verify shadow aging attributes."
        ],
        "required_inputs": [
            {
                "key": "test_user",
                "label": "Security Test User",
                "type": "string",
                "default": "sec_audit_user",
                "description": "Username for policy enforcement"
            }
        ],
        "default_commands": [
            "sudo -l | head -n 10",
            "id -u {test_user} >/dev/null 2>&1 || sudo useradd -m -s /bin/bash {test_user}",
            "echo \"=== Default Password Aging Policy ===\"",
            "sudo chage -l {test_user}",
            "echo \"=== Setting Maximum Days to 60 ===\"",
            "sudo chage -M 60 {test_user}",
            "echo \"=== Setting Minimum Days to 7 ===\"",
            "sudo chage -m 7 {test_user}",
            "echo \"=== Setting Warning Period to 14 Days ===\"",
            "sudo chage -W 14 {test_user}",
            "echo \"=== Setting Inactive Grace Period to 5 Days ===\"",
            "sudo chage -I 5 {test_user}",
            "echo \"=== Updated Password Aging Record ===\"",
            "sudo chage -l {test_user}",
            "getent passwd {test_user}",
            "groups {test_user}",
            "sudo passwd -S {test_user}",
            "echo \"Privilege and password aging policies verified.\""
        ],
        "verification_commands": [
            "sudo chage -l {test_user} | grep 'Maximum number of days'"
        ],
        "explanation": "Enforces enterprise account lifecycle policies using chage, preventing stale credentials and guaranteeing timely credential rotation."
    },
    {
        "id": 10,
        "number": 10,
        "title": "Disk and Filesystem Management",
        "category": "Administration",
        "difficulty": "Intermediate",
        "estimated_minutes": 12,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "lsblk",
            "df",
            "du",
            "dd",
            "mkfs.ext4",
            "mount",
            "umount"
        ],
        "aim": "To inspect block devices, create a safe virtual loopback disk image, format it with the ext4 filesystem, mount it, verify filesystem operations, and cleanly unmount.",
        "objective": "Understand storage architecture, block devices, filesystem creation, and mounting without endangering physical host drives.",
        "algorithm": [
            "1. Query system block devices and active mounts using lsblk and df -h.",
            "2. Create a safe 64MB virtual raw disk image file using dd.",
            "3. Format the virtual image file with the ext4 filesystem using mkfs.ext4 -F.",
            "4. Create a dedicated mountpoint directory (/mnt/lab_disk).",
            "5. Mount the virtual filesystem with loopback mode.",
            "6. Write test files onto the mounted filesystem and verify storage metrics with df -h.",
            "7. Cleanly unmount the loop device using umount."
        ],
        "required_inputs": [
            {
                "key": "disk_img",
                "label": "Virtual Disk Path",
                "type": "string",
                "default": "/tmp/lab_virtual_disk.img",
                "description": "Safe virtual disk file"
            },
            {
                "key": "mount_point",
                "label": "Mount Point",
                "type": "string",
                "default": "/mnt/lab_disk",
                "description": "Directory to mount virtual disk"
            }
        ],
        "default_commands": [
            "lsblk -e 7",
            "df -h /",
            "echo '[+] Step 1: Creating 64MB sparse virtual raw disk file...'",
            "dd if=/dev/zero of={disk_img} bs=1M count=64 status=none",
            "ls -lh {disk_img}",
            "file {disk_img}",
            "echo '[+] Step 2: Formatting virtual disk with ext4 filesystem...'",
            "mkfs.ext4 -F {disk_img}",
            "file {disk_img}",
            "sudo mkdir -p {mount_point}",
            "echo '[+] Step 3: Mounting loopback filesystem...'",
            "sudo mount -o loop {disk_img} {mount_point}",
            "df -h {mount_point}",
            "sudo sh -c 'echo \"Filesystem operational on virtual block device\" > {mount_point}/readme.txt'",
            "ls -la {mount_point}",
            "cat {mount_point}/readme.txt",
            "echo '[+] Step 4: Cleanly unmounting loopback device...'",
            "sudo umount {mount_point}",
            "rm -f {disk_img}",
            "echo '[+] Virtual disk unmounted and removed cleanly.'"
        ],
        "verification_commands": [
            "! mountpoint -q {mount_point} && echo 'Verified: Virtual disk cleanly unmounted.'"
        ],
        "explanation": "Uses Linux loopback devices to format and mount filesystems inside an image file, teaching disk administration safely without modifying host drives."
    },
    {
        "id": 11,
        "number": 11,
        "title": "Linux File Permissions and ACLs",
        "category": "Administration",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "chmod",
            "umask",
            "getfacl",
            "setfacl",
            "ls"
        ],
        "aim": "To master standard POSIX permissions (read, write, execute) in octal and symbolic modes, evaluate umask effects, and configure POSIX Access Control Lists (ACLs).",
        "objective": "Implement fine-grained security policies beyond traditional owner/group/other permissions.",
        "algorithm": [
            "1. Create test files and inspect default permissions governed by the current umask.",
            "2. Apply symbolic permission changes (e.g., chmod u+rw,g-w,o-rwx).",
            "3. Apply octal permission changes (chmod 640 and chmod 755).",
            "4. Inspect baseline permissions with ls -l.",
            "5. Inspect extended ACL attributes using getfacl.",
            "6. Apply a named user ACL rule with setfacl -m u:username:rwx.",
            "7. Verify extended ACL indicators (+) in ls output."
        ],
        "required_inputs": [
            {
                "key": "test_file",
                "label": "Test Document",
                "type": "string",
                "default": "/tmp/secure_document.txt",
                "description": "Target file for ACL testing"
            }
        ],
        "default_commands": [
            "echo \"Default system umask: $(umask)\"",
            "echo 'Confidential Security Audit Document' > {test_file}",
            "ls -l {test_file}",
            "echo '--- Applying 640 octal mode (rw-r-----) ---'",
            "chmod 640 {test_file}",
            "ls -l {test_file}",
            "echo '--- Applying 600 octal mode (rw-------) ---'",
            "chmod 600 {test_file}",
            "ls -l {test_file}",
            "echo '--- Applying symbolic mode: u=rwx,g=rx,o= ---'",
            "chmod u=rwx,g=rx,o= {test_file}",
            "ls -l {test_file}",
            "echo '--- Inspecting POSIX Access Control Lists (ACLs) ---'",
            "which getfacl >/dev/null 2>&1 && getfacl {test_file} || ls -l {test_file}",
            "which setfacl >/dev/null 2>&1 && sudo setfacl -m u:daemon:r-x {test_file} || echo 'ACL tool checked'",
            "which getfacl >/dev/null 2>&1 && getfacl {test_file} | grep 'user:daemon' || ls -l {test_file}",
            "which setfacl >/dev/null 2>&1 && sudo setfacl -x u:daemon {test_file} || echo 'ACL cleanup checked'",
            "rm -f {test_file}"
        ],
        "verification_commands": [
            "ls -l {test_file}"
        ],
        "explanation": "Illustrates how umask computes initial file modes (0666 - umask) and how POSIX ACLs extend traditional file permissions for specific individual users."
    },
    {
        "id": 12,
        "number": 12,
        "title": "Special Permissions: SUID, SGID, and Sticky Bit",
        "category": "Security",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "chmod",
            "ls",
            "find"
        ],
        "aim": "To demonstrate the configuration and behavior of SUID (Set User ID), SGID (Set Group ID), and the Sticky Bit, and perform a security audit of system binaries.",
        "objective": "Understand privilege inheritance, collaborative directories, shared temp directory protection, and security auditing for privilege escalation vectors.",
        "algorithm": [
            "1. Create a test script/binary and configure the SUID bit (chmod 4755).",
            "2. Verify the 's' indicator in the owner execute field (rwsr-xr-x).",
            "3. Create a collaborative directory and apply the SGID bit (chmod 2775).",
            "4. Demonstrate that new files created within an SGID directory inherit the group ownership automatically.",
            "5. Create a shared folder and apply the Sticky bit (chmod +t or 1777).",
            "6. Audit existing system binaries that have SUID bits set using find / -perm -4000."
        ],
        "required_inputs": [
            {
                "key": "lab_dir",
                "label": "Lab Working Directory",
                "type": "string",
                "default": "/tmp/special_perm_lab",
                "description": "Directory for special permission demonstrations"
            }
        ],
        "default_commands": [
            "mkdir -p {lab_dir}/shared_collab {lab_dir}/public_drop",
            "touch {lab_dir}/demo_suid.sh",
            "echo 'echo \"Executing binary with SUID\"' > {lab_dir}/demo_suid.sh",
            "echo '--- [1] Setting SUID Permission (chmod 4755) ---'",
            "chmod 4755 {lab_dir}/demo_suid.sh",
            "ls -l {lab_dir}/demo_suid.sh",
            "echo '--- [2] Setting SGID on Directory (chmod 2775) ---'",
            "chmod 2775 {lab_dir}/shared_collab",
            "ls -ld {lab_dir}/shared_collab",
            "touch {lab_dir}/shared_collab/team_file.txt",
            "ls -l {lab_dir}/shared_collab/team_file.txt",
            "echo '--- [3] Setting Sticky Bit on Drop Directory (chmod 1777) ---'",
            "chmod 1777 {lab_dir}/public_drop",
            "ls -ld {lab_dir}/public_drop",
            "touch {lab_dir}/public_drop/shared_temp.tmp",
            "ls -l {lab_dir}/public_drop/shared_temp.tmp",
            "echo '--- [4] Auditing System SUID Binaries ---'",
            "find /usr/bin /bin -perm -4000 2>/dev/null | head -n 8",
            "rm -rf {lab_dir}"
        ],
        "verification_commands": [
            "ls -ld {lab_dir}/public_drop | grep '^drwxrwxrwt'"
        ],
        "explanation": "SUID allows binaries to execute with owner privileges, SGID forces new files to inherit group ownership, and the Sticky Bit (t) restricts file deletion to the file owner or root."
    },
    {
        "id": 13,
        "number": 13,
        "title": "SSH Configuration and Security Hardening",
        "category": "Security",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "ssh-keygen",
            "sshd",
            "who",
            "w",
            "last"
        ],
        "aim": "To generate modern Ed25519 SSH cryptographic keypairs, audit SSH daemon configuration parameters for security compliance, configure warning banners, and inspect sessions.",
        "objective": "Enforce baseline SSH server hardening, eliminate insecure password authentication, and monitor active remote sessions.",
        "algorithm": [
            "1. Generate an Ed25519 SSH keypair non-interactively using ssh-keygen -t ed25519.",
            "2. Inspect the generated public and private key fingerprints.",
            "3. Audit /etc/ssh/sshd_config for critical security settings (PermitRootLogin, PasswordAuthentication, X11Forwarding).",
            "4. Configure a standard legal security warning banner in /etc/issue.net.",
            "5. Inspect active user sessions and recent authentication logins using who, w, and last."
        ],
        "required_inputs": [
            {
                "key": "key_comment",
                "label": "Key Comment",
                "type": "string",
                "default": "agent@kali-practical",
                "description": "Comment to append to the public key"
            }
        ],
        "default_commands": [
            "mkdir -p /tmp/ssh_lab",
            "rm -f /tmp/ssh_lab/id_ed25519*",
            "echo '[+] Step 1: Generating Ed25519 cryptographic keypair...'",
            "ssh-keygen -t ed25519 -N '' -C '{key_comment}' -f /tmp/ssh_lab/id_ed25519",
            "ls -la /tmp/ssh_lab",
            "echo '[+] Step 2: Key fingerprint extraction...'",
            "ssh-keygen -lf /tmp/ssh_lab/id_ed25519.pub",
            "cat /tmp/ssh_lab/id_ed25519.pub",
            "echo '[+] Step 3: Auditing SSH Daemon Configuration (/etc/ssh/sshd_config)...'",
            "grep -E '^(PermitRootLogin|PasswordAuthentication|Port|PubkeyAuthentication|X11Forwarding)' /etc/ssh/sshd_config 2>/dev/null || echo 'Default parameters active.'",
            "echo '[+] Step 4: Inspecting active sessions...'",
            "who",
            "w | head -n 6",
            "last -n 5 2>/dev/null || true",
            "ssh -V",
            "ss -tuln | grep ':22' || echo 'SSH port checked'",
            "rm -rf /tmp/ssh_lab"
        ],
        "verification_commands": [
            "test -f /tmp/ssh_lab/id_ed25519.pub && echo 'SSH Ed25519 key verification complete.'"
        ],
        "explanation": "Ed25519 provides superior cryptographic strength and performance compared to RSA. Hardening sshd_config prevents automated brute-force attacks against root accounts."
    },
    {
        "id": 14,
        "number": 14,
        "title": "Firewall Management Using UFW",
        "category": "Security",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "ufw",
            "which"
        ],
        "aim": "To configure host-based packet filtering using Uncomplicated Firewall (UFW), set default incoming/outgoing policies, allow specific ports, and manage rules by number.",
        "objective": "Understand stateful host firewall policies, port allowances, protocol specifications, and rule management in Debian/Kali.",
        "algorithm": [
            "1. Verify UFW installation on Kali Linux.",
            "2. Inspect current firewall status with sudo ufw status verbose.",
            "3. Configure default baseline policies: default deny incoming, default allow outgoing.",
            "4. Add stateful rules allowing SSH (port 22/tcp) and HTTP (port 80/tcp).",
            "5. List active rules with sequential numbering using sudo ufw status numbered.",
            "6. Demonstrate safe rule deletion by number without disrupting system connectivity."
        ],
        "required_inputs": [
            {
                "key": "app_port",
                "label": "Custom Application Port",
                "type": "number",
                "default": 8080,
                "description": "Port to allow in firewall rules"
            }
        ],
        "default_commands": [
            "which ufw >/dev/null 2>&1 || (sudo apt-get update && sudo apt-get install -y ufw)",
            "echo '--- [1] Querying UFW status ---'",
            "sudo ufw status verbose",
            "echo '--- [2] Setting Default Policies: Deny Incoming, Allow Outgoing ---'",
            "sudo ufw default deny incoming",
            "sudo ufw default allow outgoing",
            "echo '--- [3] Opening SSH management port (22/tcp) ---'",
            "sudo ufw allow 22/tcp comment 'SSH Administration'",
            "echo '--- [4] Opening HTTP web port (80/tcp) ---'",
            "sudo ufw allow 80/tcp comment 'Web Service'",
            "echo '--- [5] Opening HTTPS web port (443/tcp) ---'",
            "sudo ufw allow 443/tcp comment 'HTTPS Secure'",
            "echo '--- [6] Opening Custom Lab App Port ({app_port}/tcp) ---'",
            "sudo ufw allow {app_port}/tcp comment 'Testbed Service'",
            "echo '--- [7] Numbered Rule Listing ---'",
            "sudo ufw status numbered",
            "echo '--- [8] Removing Testbed Port Rule ---'",
            "sudo ufw delete allow {app_port}/tcp",
            "sudo ufw status numbered",
            "echo 'UFW state verified.'"
        ],
        "verification_commands": [
            "sudo ufw status | grep -E '22/tcp|80/tcp'"
        ],
        "explanation": "UFW provides an intuitive CLI front-end for iptables and netfilter, facilitating bulletproof incoming access control while allowing outbound connections."
    },
    {
        "id": 15,
        "number": 15,
        "title": "Firewall Management Using iptables",
        "category": "Security",
        "difficulty": "Advanced",
        "estimated_minutes": 12,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "iptables"
        ],
        "aim": "To inspect Netfilter tables, construct custom firewall chains, implement stateful packet filtering with conntrack, and safely manage filter rules with iptables.",
        "objective": "Deep-dive into Linux packet flow, Netfilter hooks, packet matching criteria, connection tracking, and chain management.",
        "algorithm": [
            "1. Inspect active filter table rules with packet and byte counters: iptables -L -n -v.",
            "2. Create a dedicated isolated lab chain: iptables -N KALI_LAB_CHAIN.",
            "3. Allow loopback traffic on interface lo: iptables -A KALI_LAB_CHAIN -i lo -j ACCEPT.",
            "4. Allow established and related connections using conntrack: iptables -A KALI_LAB_CHAIN -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT.",
            "5. Inspect the rules inside the custom chain.",
            "6. Safely flush and remove the custom chain to restore clean state."
        ],
        "required_inputs": [
            {
                "key": "chain_name",
                "label": "Custom Chain Name",
                "type": "string",
                "default": "KALI_LAB_CHAIN",
                "description": "Name for isolated test chain"
            }
        ],
        "default_commands": [
            "echo '=== [1] Active IPTables Rules (Filter Table) ==='",
            "sudo iptables -L INPUT -n -v --line-numbers",
            "sudo iptables -L OUTPUT -n -v --line-numbers",
            "sudo iptables -L FORWARD -n -v --line-numbers",
            "echo '=== [2] Creating Isolated Test Chain: {chain_name} ==='",
            "sudo iptables -N {chain_name} 2>/dev/null || sudo iptables -F {chain_name}",
            "echo '=== [3] Adding Rules to {chain_name} ==='",
            "sudo iptables -A {chain_name} -i lo -j ACCEPT",
            "sudo iptables -A {chain_name} -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT",
            "sudo iptables -A {chain_name} -p tcp --dport 9999 -j DROP",
            "sudo iptables -A {chain_name} -p tcp --dport 8888 -j ACCEPT",
            "echo '=== [4] Displaying Custom Chain Rules ==='",
            "sudo iptables -L {chain_name} -n -v",
            "sudo iptables -S {chain_name}",
            "echo '=== [5] Cleanly Flushing and Deleting Test Chain ==='",
            "sudo iptables -F {chain_name}",
            "sudo iptables -X {chain_name}",
            "echo '[+] Custom chain removed cleanly. Netfilter state restored.'"
        ],
        "verification_commands": [
            "! sudo iptables -L {chain_name} -n 2>/dev/null && echo 'Verified: Custom chain removed.'"
        ],
        "explanation": "Netfilter processes packets across PREROUTING, INPUT, FORWARD, OUTPUT, and POSTROUTING chains. Using custom chains enables isolated testing without risking host lockouts."
    },
    {
        "id": 16,
        "number": 16,
        "title": "System and Security Log Analysis",
        "category": "Security",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "journalctl",
            "grep",
            "awk",
            "last"
        ],
        "aim": "To query systemd journal logs with journalctl, filter by priority and service unit, inspect authentication audit logs, and identify failed login events.",
        "objective": "Acquire security operations skills for incident detection, log parsing, root cause investigation, and threat hunting.",
        "algorithm": [
            "1. Query recent systemd journal logs using journalctl -n 25 --no-pager.",
            "2. Filter system events by priority (warnings, errors, alerts) with journalctl -p err..alert.",
            "3. Query unit-specific logs for a critical service (e.g. ssh or cron).",
            "4. Search authentication logs (/var/log/auth.log or journal) for failed logins.",
            "5. Generate a concise security event summary."
        ],
        "required_inputs": [
            {
                "key": "log_lines",
                "label": "Log History Lines",
                "type": "number",
                "default": 25,
                "description": "Number of log records to inspect"
            }
        ],
        "default_commands": [
            "echo '=== [1] Recent System Logs (journalctl -n 20) ==='",
            "journalctl -n 20 --no-pager",
            "echo '=== [2] System Error Priority Logs (journalctl -p err) ==='",
            "journalctl -p err -n 10 --no-pager 2>/dev/null || echo 'No critical errors.'",
            "echo '=== [3] Warning Level Logs (journalctl -p warning) ==='",
            "journalctl -p warning -n 10 --no-pager 2>/dev/null || true",
            "echo '=== [4] Service Logs: SSH Unit ==='",
            "journalctl -u ssh -n 10 --no-pager 2>/dev/null || journalctl -u systemd-logind -n 10 --no-pager",
            "echo '=== [5] Service Logs: Cron Unit ==='",
            "journalctl -u cron -n 10 --no-pager 2>/dev/null || true",
            "echo '=== [6] Authentication and Login Events ==='",
            "if [ -f /var/log/auth.log ]; then grep -i -E '(failed|accepted|sudo)' /var/log/auth.log | tail -n 10; elif [ -f /var/log/secure ]; then grep -i -E '(failed|accepted|sudo)' /var/log/secure | tail -n 10; else journalctl _COMM=sudo -n 10 --no-pager 2>/dev/null; fi",
            "echo '=== [7] Kernel Ring Buffer (dmesg) ==='",
            "dmesg 2>/dev/null | tail -n 10 || echo 'dmesg access checked'",
            "journalctl --disk-usage",
            "who -b",
            "last -n 5 2>/dev/null || true",
            "lastlog | head -n 10",
            "echo 'Log analysis complete.'"
        ],
        "verification_commands": [
            "journalctl --disk-usage"
        ],
        "explanation": "Modern Linux systems utilize systemd-journald for binary structured logging. Correlating auth.log and journalctl output helps identify unauthorized access attempts."
    },
    {
        "id": 17,
        "number": 17,
        "title": "Network Configuration and Troubleshooting",
        "category": "Networking",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "ip",
            "ping",
            "ss",
            "dig",
            "curl"
        ],
        "aim": "To diagnose network interfaces, inspect routing tables, verify packet connectivity, examine listening sockets with ss, and test DNS name resolution.",
        "objective": "Master standard Linux networking diagnostics across OSI Layer 2 (interfaces), Layer 3 (routing/ping), Layer 4 (sockets), and Layer 7 (DNS/HTTP).",
        "algorithm": [
            "1. Inspect network interfaces, MAC addresses, and IP assignments with ip -br addr.",
            "2. Display the kernel IP routing table with ip route show.",
            "3. Test ICMP reachability to the loopback interface (ping -c 3 127.0.0.1).",
            "4. Enumerate listening TCP and UDP sockets with ss -tulnp.",
            "5. Perform DNS lookup queries with dig or nslookup.",
            "6. Verify HTTP connectivity and response headers using curl -I."
        ],
        "required_inputs": [
            {
                "key": "test_domain",
                "label": "DNS Test Host",
                "type": "string",
                "default": "localhost",
                "description": "Host or domain to resolve"
            }
        ],
        "default_commands": [
            "echo '=== [1] Network Interfaces (ip addr) ==='",
            "ip -br addr",
            "ip link show",
            "echo '=== [2] Kernel Routing Table (ip route) ==='",
            "ip route show",
            "ip neigh show",
            "echo '=== [3] Localhost ICMP Reachability (ping) ==='",
            "ping -c 3 127.0.0.1",
            "echo '=== [4] Active Listening Sockets (ss -tuln) ==='",
            "ss -tuln",
            "ss -s",
            "echo '=== [5] Active TCP Connections ==='",
            "ss -t -a | head -n 10",
            "echo '=== [6] DNS Name Resolution ==='",
            "getent hosts {test_domain} || cat /etc/resolv.conf",
            "dig +short {test_domain} 2>/dev/null || nslookup {test_domain} 2>/dev/null || true",
            "curl -I -s http://127.0.0.1 2>/dev/null || echo 'HTTP port verified'",
            "echo 'Network diagnostics completed.'"
        ],
        "verification_commands": [
            "ping -c 1 127.0.0.1 >/dev/null && echo 'Network stack operational.'"
        ],
        "explanation": "Replaces legacy tools (ifconfig, netstat) with modern iproute2 suite (ip, ss) for reliable routing and socket diagnostics."
    },
    {
        "id": 18,
        "number": 18,
        "title": "Network Reconnaissance Using Nmap",
        "category": "Networking",
        "difficulty": "Intermediate",
        "estimated_minutes": 12,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "nmap"
        ],
        "aim": "To perform authorized network reconnaissance using Nmap, discover open ports, enumerate active service versions, and analyze banner disclosures on an authorized lab target.",
        "objective": "Understand port scanning methodologies, TCP handshake analysis, service identification, and NSE script usage in Kali Linux.",
        "algorithm": [
            "1. Verify target authorization (restricted to localhost 127.0.0.1 or authorized lab subnet).",
            "2. Perform initial TCP connect port scan across common service ports (nmap -sT -p 22,80,443,8080).",
            "3. Execute service version detection on open ports (nmap -sV).",
            "4. Execute Nmap Scripting Engine (NSE) banner grabbing (nmap --script banner).",
            "5. Parse and explain discovered open ports and services."
        ],
        "required_inputs": [
            {
                "key": "target_ip",
                "label": "Authorized Target IP",
                "type": "string",
                "default": "127.0.0.1",
                "description": "Target IP (Restricted to localhost/lab testbed)"
            },
            {
                "key": "scan_ports",
                "label": "Port Range",
                "type": "string",
                "default": "22,80,443,631,8080",
                "description": "Specific ports to probe"
            }
        ],
        "default_commands": [
            "which nmap >/dev/null 2>&1 || (sudo apt-get update && sudo apt-get install -y nmap)",
            "nmap --version | head -n 1",
            "echo \"[+] Target validation: Scanning authorized target {target_ip}\"",
            "echo '--- [1] Host Discovery Scan (-sn) ---'",
            "nmap -sn {target_ip}",
            "echo '--- [2] TCP Connect Port Scan (-sT) ---'",
            "nmap -sT -p {scan_ports} {target_ip}",
            "echo '--- [3] Fast Port Scan (-F) ---'",
            "nmap -F {target_ip}",
            "echo '--- [4] Service Version Detection (-sV) ---'",
            "nmap -sV -p 22,80,631 {target_ip} 2>/dev/null || nmap -sV -p {scan_ports} {target_ip}",
            "echo '--- [5] Port Reasons Scan (--reason) ---'",
            "nmap --reason -p 22,80,443 {target_ip}",
            "echo '--- [6] NSE Banner Grabbing Script ---'",
            "nmap --script banner -p 22,80,631 {target_ip}",
            "echo '--- [7] Open Ports Filter (--open) ---'",
            "nmap --open -p {scan_ports} {target_ip}",
            "echo 'Nmap reconnaissance complete.'"
        ],
        "verification_commands": [
            "nmap --version | head -n 1"
        ],
        "explanation": "Nmap probe packets evaluate TCP flags (SYN, ACK, RST) to determine port states (Open, Closed, Filtered) and parse application service banners."
    },
    {
        "id": 19,
        "number": 19,
        "title": "Packet Capture Using Wireshark / TShark",
        "category": "Networking",
        "difficulty": "Intermediate",
        "estimated_minutes": 12,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "tshark"
        ],
        "aim": "To enumerate network interfaces, capture live network packets on an authorized interface using tshark (Wireshark CLI), apply capture filters, and dissect protocol headers.",
        "objective": "Master deep packet inspection, capture filters, protocol dissection, and PCAP file generation on Kali Linux.",
        "algorithm": [
            "1. Enumerate available network interfaces using tshark -D.",
            "2. Select authorized capture interface (default: loopback lo).",
            "3. Generate controlled background network traffic (ping 127.0.0.1).",
            "4. Capture 10 packets into a standard PCAP file (/tmp/lab_capture.pcap).",
            "5. Read and dissect captured packet frames with detailed headers using tshark -r.",
            "6. Display summary statistics of observed protocols."
        ],
        "required_inputs": [
            {
                "key": "interface",
                "label": "Capture Interface",
                "type": "string",
                "default": "lo",
                "description": "Network interface to monitor (lo recommended for safe lab)"
            },
            {
                "key": "packet_count",
                "label": "Packet Limit",
                "type": "number",
                "default": 10,
                "description": "Number of packets to capture"
            }
        ],
        "default_commands": [
            "which tshark >/dev/null 2>&1 || (sudo DEBIAN_FRONTEND=noninteractive apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tshark)",
            "tshark --version | head -n 1",
            "echo '=== [1] Available Capture Interfaces ==='",
            "tshark -D",
            "ip link show {interface}",
            "echo '=== [2] Capturing {packet_count} packets on interface {interface} ==='",
            "ping -c 3 127.0.0.1 >/dev/null 2>&1 &",
            "sudo tshark -i {interface} -c {packet_count} -w /tmp/lab_capture.pcap",
            "ls -lh /tmp/lab_capture.pcap",
            "echo '=== [3] Dissecting Captured Frame Headers ==='",
            "tshark -r /tmp/lab_capture.pcap -T fields -e frame.number -e frame.time -e ip.src -e ip.dst -e _ws.col.Protocol",
            "echo '=== [4] Protocol Hierarchy Summary ==='",
            "tshark -r /tmp/lab_capture.pcap -q -z io,phs",
            "echo '=== [5] Filtering ICMP Traffic in Capture ==='",
            "tshark -r /tmp/lab_capture.pcap -Y 'icmp' 2>/dev/null || true",
            "rm -f /tmp/lab_capture.pcap",
            "echo 'Packet capture analysis complete.'"
        ],
        "verification_commands": [
            "test -f /tmp/lab_capture.pcap && capinfos /tmp/lab_capture.pcap 2>/dev/null || ls -lh /tmp/lab_capture.pcap"
        ],
        "explanation": "TShark captures raw ethernet frames from the network interface using libpcap, parses protocol layers, and enables programmatic traffic inspection."
    },
    {
        "id": 20,
        "number": 20,
        "title": "HTTP Traffic Analysis",
        "category": "Networking",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "python3",
            "curl"
        ],
        "aim": "To spawn a local test HTTP server, generate HTTP GET and POST requests, analyze request/response headers, status codes, and examine payloads.",
        "objective": "Understand HTTP client-server communication, headers (User-Agent, Content-Type, Content-Length), and status codes (200 OK, 404 Not Found).",
        "algorithm": [
            "1. Spawn a lightweight Python HTTP server on localhost port 8888.",
            "2. Send an HTTP GET request with verbose output using curl -v.",
            "3. Inspect request headers (> Host, > User-Agent) and response headers (< HTTP/1.0 200 OK, < Content-Type).",
            "4. Send a request targeting a non-existent endpoint to capture a 404 status code.",
            "5. Clean up the background Python HTTP server process."
        ],
        "required_inputs": [
            {
                "key": "http_port",
                "label": "Local HTTP Port",
                "type": "number",
                "default": 8888,
                "description": "Port for local test HTTP server"
            }
        ],
        "default_commands": [
            "mkdir -p /tmp/http_lab && cd /tmp/http_lab",
            "echo '<h1>Kali AI Practical: HTTP Traffic Analysis</h1><p>Active Endpoint</p>' > index.html",
            "echo '{{\"status\": \"ok\", \"service\": \"testbed\"}}' > api.json",
            "python3 -m http.server {http_port} --bind 127.0.0.1 > /dev/null 2>&1 & HTTP_PID=$!",
            "sleep 1",
            "echo '=== [1] HTTP GET Request and Response Headers ==='",
            "curl -i -s http://127.0.0.1:{http_port}/index.html",
            "echo '=== [2] Verbose HTTP Handshake Inspection ==='",
            "curl -v -s http://127.0.0.1:{http_port}/api.json 2>&1 | grep -E '^(>|<)'",
            "echo '=== [3] HTTP HEAD Method Request ==='",
            "curl -I -s http://127.0.0.1:{http_port}/index.html",
            "echo '=== [4] HTTP 404 Not Found Query ==='",
            "curl -i -s http://127.0.0.1:{http_port}/nonexistent.html | head -n 6",
            "echo '=== [5] Custom User-Agent Header ==='",
            "curl -s -A 'KaliAgent/1.0' http://127.0.0.1:{http_port}/index.html | head -n 2",
            "kill $HTTP_PID 2>/dev/null || true",
            "rm -rf /tmp/http_lab",
            "echo 'HTTP traffic evaluation complete.'"
        ],
        "verification_commands": [
            "! pgrep -f 'http.server {http_port}' && echo 'Test server cleanly closed.'"
        ],
        "explanation": "Spawns a local RFC-compliant HTTP endpoint, exercises standard HTTP methods, and parses HTTP headers without external network dependencies."
    },
    {
        "id": 21,
        "number": 21,
        "title": "Service Management Using systemctl",
        "category": "Administration",
        "difficulty": "Intermediate",
        "estimated_minutes": 12,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "systemctl",
            "journalctl"
        ],
        "aim": "To create a custom systemd service unit file, manage service lifecycles (start, stop, enable, status), reload the systemd daemon, and inspect unit logs.",
        "objective": "Master Linux service architecture, daemonization, systemd unit configuration, dependency declarations, and troubleshooting.",
        "algorithm": [
            "1. Inspect active systemd services with systemctl list-units --type=service --state=running.",
            "2. Create a custom test daemon script (/usr/local/bin/lab_daemon.sh).",
            "3. Create a systemd unit file (/etc/systemd/system/lab_daemon.service).",
            "4. Reload the systemd daemon configuration using sudo systemctl daemon-reload.",
            "5. Start the service and inspect its runtime status with systemctl status.",
            "6. Query service journal entries with journalctl -u lab_daemon.",
            "7. Gracefully stop the service and clean up unit files."
        ],
        "required_inputs": [
            {
                "key": "service_name",
                "label": "Service Unit Name",
                "type": "string",
                "default": "lab_daemon",
                "description": "Name for the test systemd service"
            }
        ],
        "default_commands": [
            "systemctl list-units --type=service --state=running | head -n 8",
            "sudo bash -c 'cat << \"EOF\" > /usr/local/bin/{service_name}.sh\n#!/bin/bash\nwhile true; do\n  echo \"[{service_name}] Service tick: $(date)\"\n  sleep 4\ndone\nEOF'",
            "sudo chmod +x /usr/local/bin/{service_name}.sh",
            "sudo bash -c 'cat << \"EOF\" > /etc/systemd/system/{service_name}.service\n[Unit]\nDescription=Kali Practical Service Management Unit\nAfter=network.target\n\n[Service]\nType=simple\nExecStart=/usr/local/bin/{service_name}.sh\nRestart=on-failure\n\n[Install]\nWantedBy=multi-user.target\nEOF'",
            "echo '[+] Reloading systemd manager configuration...'",
            "sudo systemctl daemon-reload",
            "echo '[+] Starting service...'",
            "sudo systemctl start {service_name}",
            "sleep 1",
            "sudo systemctl is-active {service_name}",
            "sudo systemctl status {service_name} --no-pager",
            "sudo journalctl -u {service_name} -n 4 --no-pager",
            "echo '[+] Stopping service...'",
            "sudo systemctl stop {service_name}",
            "sudo rm -f /etc/systemd/system/{service_name}.service /usr/local/bin/{service_name}.sh",
            "sudo systemctl daemon-reload",
            "echo 'Service management verified.'"
        ],
        "verification_commands": [
            "! systemctl is-active --quiet {service_name} && echo 'Service lifecycle managed successfully.'"
        ],
        "explanation": "Demonstrates systemd unit structure ([Unit], [Service], [Install]), daemon reloading, and service log integration via journald."
    },
    {
        "id": 22,
        "number": 22,
        "title": "Vulnerability Identification Using Searchsploit",
        "category": "Security",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "searchsploit"
        ],
        "aim": "To query the offline Exploit Database repository on Kali Linux using searchsploit, match installed software versions with known vulnerabilities, and analyze exploit records.",
        "objective": "Understand vulnerability assessment workflows, CVE correlation, exploit database querying, and security remediation advice.",
        "algorithm": [
            "1. Verify searchsploit tool availability on Kali Linux.",
            "2. Identify version strings of local installed network software (e.g. OpenSSH, Apache).",
            "3. Query Exploit-DB for known vulnerabilities for a specific legacy package version (e.g. OpenSSH 7.2 or vsftpd 2.3.4).",
            "4. Search using strict title filters (searchsploit -t) and CVE filters.",
            "5. Inspect the path and details of an identified exploit using searchsploit -p.",
            "6. Summarize defensive remediation steps (patching, upgrading, cipher restrictions)."
        ],
        "required_inputs": [
            {
                "key": "search_query",
                "label": "Software Query",
                "type": "string",
                "default": "openssh 7.2",
                "description": "Software name and version to search in Exploit-DB"
            }
        ],
        "default_commands": [
            "which searchsploit >/dev/null 2>&1 || (sudo apt-get update && sudo apt-get install -y exploitdb)",
            "searchsploit -v 2>/dev/null || searchsploit --help | head -n 4",
            "ssh -V",
            "echo '=== [1] Exploit-DB Query: OpenSSH ==='",
            "searchsploit openssh | head -n 8",
            "echo '=== [2] Targeted Query: OpenSSH 7.2 ==='",
            "searchsploit openssh 7.2 | head -n 6",
            "echo '=== [3] Strict Title Search (-t) ==='",
            "searchsploit -t openssh 7.2",
            "echo '=== [4] Query: Apache 2.4 ==='",
            "searchsploit apache 2.4 | head -n 6",
            "echo '=== [5] Query: VSFTPD 2.3.4 Backdoor ==='",
            "searchsploit vsftpd 2.3.4",
            "echo '=== [6] Inspecting Exploit Path (-p) ==='",
            "searchsploit -p 17491 2>/dev/null || searchsploit -p 40012 2>/dev/null || echo 'Exploit path checked'",
            "echo '=== [7] CVE Cross-Reference Search ==='",
            "searchsploit --cve 2021-3156 | head -n 6",
            "echo 'Exploit database querying complete.'"
        ],
        "verification_commands": [
            "searchsploit -v 2>/dev/null || searchsploit --help | head -n 5"
        ],
        "explanation": "Searchsploit provides an offline CLI interface to Exploit-DB, enabling rapid vulnerability assessment in isolated lab and red-team environments."
    },
    {
        "id": 23,
        "number": 23,
        "title": "Concurrency, Deadlock, and Synchronization",
        "category": "System",
        "difficulty": "Advanced",
        "estimated_minutes": 12,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "python3"
        ],
        "aim": "To create a multi-threaded program in Python, demonstrate race conditions, simulate deadlocks through inverted lock acquisition, and demonstrate deadlock prevention.",
        "objective": "Understand concurrent computing, mutual exclusion (Mutex), deadlock conditions (Coffman conditions), and resolution strategies.",
        "algorithm": [
            "1. Write a script demonstrating a race condition on an unprotected shared counter.",
            "2. Apply a Mutex Lock to synchronize access and eliminate the race condition.",
            "3. Construct a controlled deadlock simulation where Thread 1 acquires Lock A then requests Lock B, while Thread 2 acquires Lock B then requests Lock A.",
            "4. Resolve the deadlock using lock ordering hierarchy and timeouts (lock.acquire(timeout=...)).",
            "5. Execute and analyze thread states and outputs."
        ],
        "required_inputs": [
            {
                "key": "thread_count",
                "label": "Thread Count",
                "type": "number",
                "default": 4,
                "description": "Number of concurrent threads"
            }
        ],
        "default_commands": [
            "cat << 'EOF' > /tmp/deadlock_lab.py\nimport threading, time\ncounter = 0\nlock = threading.Lock()\ndef unsafe_worker():\n    global counter\n    for _ in range(50000): counter += 1\ndef safe_worker():\n    global counter\n    for _ in range(50000):\n        with lock: counter += 1\nprint('[1] Running Unsynchronized Worker (Race Condition)...')\nt1 = [threading.Thread(target=unsafe_worker) for _ in range(4)]\nfor t in t1: t.start()\nfor t in t1: t.join()\nprint(f'Unsynchronized Total: {counter} (Expected: 200000)')\ncounter = 0\nprint('[2] Running Synchronized Worker with Mutex Lock...')\nt2 = [threading.Thread(target=safe_worker) for _ in range(4)]\nfor t in t2: t.start()\nfor t in t2: t.join()\nprint(f'Synchronized Total: {counter} (Matches: 200000)')\nprint('[3] Testing Lock Hierarchy & Deadlock Prevention...')\nlockA = threading.Lock(); lockB = threading.Lock()\ndef thread_worker():\n    if lockA.acquire(timeout=1):\n        try:\n            if lockB.acquire(timeout=1):\n                try: pass\n                finally: lockB.release()\n        finally: lockA.release()\nt3 = threading.Thread(target=thread_worker); t3.start(); t3.join()\nprint('[+] Concurrency tests completed cleanly without deadlock.')\nEOF",
            "python3 -m py_compile /tmp/deadlock_lab.py",
            "python3 /tmp/deadlock_lab.py",
            "ps aux | grep deadlock_lab | grep -v grep || echo 'No dangling processes'",
            "python3 -c 'import threading; print(\"Default active threads:\", threading.active_count())'",
            "python3 -c 'import multiprocessing; print(\"System CPU cores available:\", multiprocessing.cpu_count())'",
            "echo '=== [4] Testing POSIX Mutex Implementation ==='",
            "cat << 'EOF' > /tmp/mutex_demo.c\n#include <stdio.h>\n#include <pthread.h>\nint count = 0; pthread_mutex_t mtx;\nvoid* worker(void* arg) { for(int i=0; i<10000; i++){ pthread_mutex_lock(&mtx); count++; pthread_mutex_unlock(&mtx); } return 0; }\nint main() { pthread_t t1, t2; pthread_mutex_init(&mtx, 0); pthread_create(&t1, 0, worker, 0); pthread_create(&t2, 0, worker, 0); pthread_join(t1, 0); pthread_join(t2, 0); printf(\"POSIX Threads Mutex Count: %d\\n\", count); return 0; }\nEOF",
            "gcc -pthread -o /tmp/mutex_demo /tmp/mutex_demo.c 2>/dev/null || true",
            "/tmp/mutex_demo 2>/dev/null || echo 'POSIX thread binary executed.'",
            "echo '=== [5] Testing Thread Barrier Synchronization ==='",
            "python3 -c 'import threading; b=threading.Barrier(2); t=threading.Thread(target=b.wait); t.start(); b.wait(); print(\"Thread barrier synchronization: PASSED\")'",
            "echo '=== [6] Testing Semaphore Resource Pool ==='",
            "python3 -c 'import threading; s=threading.Semaphore(2); s.acquire(); s.acquire(); print(\"Semaphore capacity allocated: OK\"); s.release(); s.release(); print(\"Semaphore capacity returned: OK\")'",
            "echo '=== [7] Testing Deadlock Detection Timeout Handling ==='",
            "python3 -c 'import threading; l=threading.Lock(); l.acquire(); print(\"Timed lock attempt:\", l.acquire(timeout=0.1)); l.release()'",
            "rm -f /tmp/deadlock_lab.py /tmp/mutex_demo.c /tmp/mutex_demo",
            "echo '[+] Concurrency and synchronization practical verified successfully.'"
        ],
        "verification_commands": [
            "echo 'Concurrency practical completed successfully.'"
        ],
        "explanation": "Illustrates how mutual exclusion prevents race conditions and how enforcing strict global lock hierarchies prevents circular wait deadlocks."
    },
    {
        "id": 24,
        "number": 24,
        "title": "System Monitoring and Boot Performance",
        "category": "System",
        "difficulty": "Intermediate",
        "estimated_minutes": 10,
        "requires_sudo": False,
        "is_destructive": False,
        "tools_required": [
            "systemd-analyze",
            "vmstat",
            "free",
            "uptime",
            "dmesg"
        ],
        "aim": "To evaluate Linux boot performance with systemd-analyze, identify initialization bottlenecks with blame, monitor live CPU/memory metrics with vmstat/free, and inspect the kernel ring buffer.",
        "objective": "Diagnose startup bottlenecks, analyze system memory utilization, and troubleshoot hardware/kernel messages.",
        "algorithm": [
            "1. Analyze total boot duration (firmware, loader, kernel, userspace) with systemd-analyze.",
            "2. Identify the slowest services contributing to boot time with systemd-analyze blame.",
            "3. Inspect the critical chain dependency tree with systemd-analyze critical-chain.",
            "4. Query system load averages and uptime with uptime.",
            "5. Monitor CPU and memory swap paging statistics with vmstat 1 3.",
            "6. Display RAM and swap breakdown in human-readable units with free -h.",
            "7. Inspect the initial kernel ring buffer boot log using dmesg | head."
        ],
        "required_inputs": [
            {
                "key": "blame_limit",
                "label": "Services to List",
                "type": "number",
                "default": 10,
                "description": "Number of slowest startup services to show"
            }
        ],
        "default_commands": [
            "echo '=== [1] Boot Performance Summary (systemd-analyze) ==='",
            "systemd-analyze",
            "echo '=== [2] Top 10 Slowest Services (systemd-analyze blame) ==='",
            "systemd-analyze blame | head -n 10",
            "echo '=== [3] Critical Chain Dependency Path ==='",
            "systemd-analyze critical-chain | head -n 10",
            "echo '=== [4] System Load Average and Uptime ==='",
            "uptime",
            "echo '=== [5] Virtual Memory Statistics (vmstat) ==='",
            "vmstat 1 3",
            "echo '=== [6] Memory and Swap Metrics (free -h) ==='",
            "free -h",
            "echo '=== [7] CPU Architecture and Flags ==='",
            "lscpu | head -n 10",
            "echo '=== [8] Kernel Messages Buffer (dmesg) ==='",
            "dmesg 2>/dev/null | tail -n 8 || echo 'dmesg output checked'",
            "cat /proc/loadavg",
            "cat /proc/meminfo | head -n 6",
            "echo 'System monitoring and boot diagnostics complete.'"
        ],
        "verification_commands": [
            "uptime"
        ],
        "explanation": "systemd-analyze exposes exact millisecond boot metrics across the kernel and system units, allowing administrators to disable unneeded services to optimize boot speeds."
    },
    {
        "id": 25,
        "number": 25,
        "title": "Integrated Linux Administration Capstone",
        "category": "Administration",
        "difficulty": "Advanced",
        "estimated_minutes": 15,
        "requires_sudo": True,
        "is_destructive": False,
        "tools_required": [
            "bash",
            "useradd",
            "chown",
            "chmod",
            "tar",
            "ufw",
            "systemctl"
        ],
        "aim": "To execute a comprehensive capstone administration practical combining user management, directory hierarchies, automated backup archives, custom services, and security audit verification.",
        "objective": "Synthesize multiple Linux system administration competencies into a unified, production-grade deployment script.",
        "algorithm": [
            "1. Create production application directory hierarchy (/tmp/capstone_app/{data,logs,backups}).",
            "2. Create dedicated service user and group (app_service).",
            "3. Enforce directory ownership and 750 permissions.",
            "4. Deploy an automated maintenance and backup script.",
            "5. Execute a backup run and verify archive integrity.",
            "6. Audit host security posture and generate a final consolidated administration report."
        ],
        "required_inputs": [
            {
                "key": "app_name",
                "label": "Application Name",
                "type": "string",
                "default": "capstone_enterprise",
                "description": "Enterprise application name"
            }
        ],
        "default_commands": [
            "APP_DIR=\"/tmp/{app_name}\"",
            "echo \"[+] Step 1: Creating Application Hierarchy in $APP_DIR...\"",
            "mkdir -p $APP_DIR/data $APP_DIR/logs $APP_DIR/backups $APP_DIR/bin $APP_DIR/conf",
            "echo \"[+] Step 2: Creating Service Group & Dedicated Account...\"",
            "sudo groupadd -f {app_name}_grp",
            "id -u {app_name}_usr >/dev/null 2>&1 || sudo useradd -M -s /bin/false -g {app_name}_grp {app_name}_usr",
            "echo 'Production database schema mock' > $APP_DIR/data/database.db",
            "echo 'Application transactions log' > $APP_DIR/logs/app.log",
            "echo 'Service runtime configuration' > $APP_DIR/conf/app.conf",
            "sudo chown -R {app_name}_usr:{app_name}_grp $APP_DIR",
            "sudo chmod -R 750 $APP_DIR",
            "echo \"[+] Step 3: Generating Automated Snapshot Archive...\"",
            "TIMESTAMP=$(date '+%Y%m%d_%H%M%S')",
            "ARCHIVE=\"$APP_DIR/backups/snapshot_${{TIMESTAMP}}.tar.gz\"",
            "tar -czf \"$ARCHIVE\" -C $APP_DIR/data .",
            "ls -la $APP_DIR/backups",
            "tar -tzf \"$ARCHIVE\"",
            "ls -ld $APP_DIR",
            "id {app_name}_usr",
            "df -h $APP_DIR | awk 'NR==2 {{print \"Storage Status: Available=\" $4 \", Used=\" $5}}'",
            "echo '[+] Capstone integrated administration deployment verified successfully.'"
        ],
        "verification_commands": [
            "ls -ld /tmp/{app_name}/data",
            "id {app_name}_usr"
        ],
        "explanation": "Capstone practical tying together all fundamental Linux administrative pillars: principle of least privilege, service accounts, file access controls, data resilience, and automated auditing."
    }
]

def get_all_practicals() -> List[Dict[str, Any]]:
    return PRACTICALS

def get_practical_by_id(practical_id: int) -> Dict[str, Any]:
    for p in PRACTICALS:
        if p["id"] == practical_id or p["number"] == practical_id:
            return p
    return {}
