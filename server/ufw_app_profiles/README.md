All firewall rules should be labeled to better manage their removal.

For one off rules, use `ufw allow 22 comment 'for SSH'` 

Alternatively, put the files in this folder into `/etc/ufw/applications.d` on your server.

Usage:
- View app profiles with `ufw app list`
- Apply firewall rules with `ufw allow "App name"`

