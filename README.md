# IgBot
A simple bot to |!ke p()$t$ and g4!n f()||oW3R$ on !n$t@9r4m.

## Installation
- clone the repository (and create a [venv](https://towardsdatascience.com/getting-started-with-python-virtual-environments-252a6bd2240))
- install requirements
```bash
$ pip install -r requirements.txt
```

## Usage
run main.py specifying the username handle `-u`, the aim number of likes per each hashtag `-l`, and whether you want or not to display the working browser `-b` (`True` for headless browser, `False` otherwise), *e.g.*
```bash
$ python3 main.py -u joeappleseed -l 50 -b True
```
for 50 likes for each hashtag without displaying the browser for @joeappleseed account.

IgBot recognize if it is the first login and, in that case, asks for the password and the preferred hashtags directly from the bash. Once provided all the necessary information, it saves the cookies for later logins.

## Logfile

IgBot automatically create a .csv file storing the time, hashtag, URL last bit, like-sender handle, and like-receiver handle for each like *e.g.*
```
2023-03-21 20:00:00,Madeinitaly,/p/Co2f2hNp__H/,joeappleseed,kimkardashian
```
(the working URL is `https://www.instagram.com/` + `p/Co2f2hNp__H/`)
### Disclaimer

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors

- [@andreacannizzo](https://www.github.com/andreacannizzo) a.k.a. Andrea C.

## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
