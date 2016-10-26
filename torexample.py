import io
import pycurl
import stem.process
from stem.util import term
SOCKS_PORT = 9050

def query(url):
	output = io.BytesIO()
	query = pycurl.Curl()
	query.setopt(pycurl.URL, url)
	query.setopt(pycurl.PROXY, 'localhost')
	query.setopt(pycurl.PROXYPORT, SOCKS_PORT)
	query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
	query.setopt(pycurl.WRITEFUNCTION, output.write)
	try:
		query.perform()
		return output.getvalue()
	except pycurl.error as exc:
		return "Unable to reach %s (%s)" %(url, exc)


def print_bootstrap_lines(line):
	if "Bootstrapped" in line:
		print(term.format(line, term.Color.BLUE))




cc = ['{ru}','{de}','{ca}','{se}','{us}']
for i in range(0,len(cc)):
        try:
                print(term.format("Starting Tor: country code: %s\n" %(cc[i]), term.Attr.BOLD))
        
                tor_process = stem.process.launch_tor_with_config(
                        tor_cmd = '/usr/local/Cellar/tor/0.2.6.10/bin/tor',
                        config = {
                                'SocksPort': str(SOCKS_PORT),
                                'ExitNodes': cc[i],
                                },
                        init_msg_handler = print_bootstrap_lines,
                        )


                print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
                print(term.format((query("https://www.atagar.com/echo.php").decode()), term.Color.BLUE))
                tor_process.kill()
                print('Tor closed.\n\n')
        except:
                try:
                        tor_process.kill()
                        print('Error: Tor closed.\n\n')
                except:
                        print('please kill tor in terminal')
                
