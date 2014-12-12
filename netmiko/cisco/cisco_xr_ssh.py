from netmiko.ssh_connection import SSHConnection
import re

class CiscoXrSSH(SSHConnection):

    def send_config_set(self, config_commands=None, commit=True):
        '''
        Send in a set of configuration commands as a list

        The commands will be executed one after the other

        Automatically exits/enters configuration mode.
        '''

        if config_commands is None:
            return ''

        # Check if already in config mode
        output = ''
        if not '(config)' in output:
            self.config_mode()
            output += self.send_command('\n', strip_prompt=False, strip_command=False)

        output += ''.join(self.send_command(a_command, strip_prompt=False,
                          strip_command=False) for a_command in config_commands)

        if commit is True:
            output += self.commit()
            return output

        return output



    def commit(self):
        '''
        Commit the entered configuration. Raise an error

        and return the failure if the commit fails.
        '''

        commit_cmd = ['\n', 'commit']

        output = ''

        output = ''.join(self.send_command(a_command, strip_prompt=False,
                         strip_command=False) for a_command in commit_cmd)

        if "Failed to commit one or more configuration" in output:
            fail_msg = self.send_command('show configuration failed',
                                         strip_prompt=False, strip_command=False)
            raise ValueError('Commit failed with the following errors:\n\n\
            {fail_msg}'.format(fail_msg=fail_msg))

        else:
            output += self.exit_config_mode()
            return output


    def normalize_linefeeds(self, a_string):
        '''
        Convert '\r\n','\r\r\n', '\n\r', or '\r' to '\n
        '''

        newline = re.compile(r'(\r\r\n|\r\n|\n\r|\r)')

        return newline.sub('\n', a_string)

















