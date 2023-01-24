import tls_client
import os
import json
import urllib
import requests
import time
from solveruwu import solve
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import atexit, random, threading
import numpy as np
from PIL import Image

os.system("cls")


class console:
    def __init__(self):
        os.system("")
        self.red = "\033[38;2;255;0;0m"
        self.green = "\033[38;2;0;255;0m"
        self.blue = "\033[38;2;0;0;255m"
        self.yellow = "\033[38;2;255;255;0m"
        self.white = "\033[38;2;200;200;200m"
        self.grey = "\033[38;2;40;40;40m"
        self.end = "\033[0m\n"
    
    def gettime(self):
        return time.strftime('%H:%M:%S', time.localtime())
    
    def warn(self,text):
        print(f"{self.grey}{self.gettime()} | {self.red}[!]{self.white} {text}",end=self.end)

    def success(self,text):
        print(f"{self.grey}{self.gettime()} | {self.green}[+]{self.white} {text}",end=self.end)

    def log(self,text):
        print(f"{self.grey}{self.gettime()} | {self.blue}[*]{self.white} {text}",end=self.end)

    def info(self,text):
        print(f"{self.grey}{self.gettime()} | {self.yellow}[?]{self.white} {text}",end=self.end)

console = console()

class hcap:
    def __init__(self,sitekey,host):
        self.sitekey = sitekey
        self.host = host
        self.session = requests.Session()
        self.client = tls_client.Session(client_identifier="chrome_108",random_tls_extension_order=True)
        self.c = self.checksiteconfig()["c"]
        self.e()
        self.cap = self.getcaptcha()
        self.download_cap()
        self.ans = self.solve("./fotoz",self.cap["requester_question"]["en"])
        if self.ans == [False for _ in range(9)]:
            console.warn(f'unsupported captcha challange ({self.cap["requester_question"]["en"]})')
            return
        console.success(f'{self.cap["requester_question"]["en"]}: {self.ans}')
        
        # fig = plt.figure(figsize=(9, 13))
        # ax = []
        # for i in range(9):
        #     img = Image.open(f'./fotoz/{i+1}.png')
        #     ax.append(fig.add_subplot(3, 3, i+1) )
        #     ax[-1].set_title(self.ans[i])
        #     plt.imshow(img)
        # plt.show()
        
        check = self.checkcaptcha()
        console.log(check.json())
    
    def checksiteconfig(self):
        headers = {
            'accept':               'application/json',
            'accept-encoding':      'gzip, deflate, br',
            'accept-language':      'en',
            'content-length':       '0',
            'content-type':         'text/plain',
            'origin':               'https://newassets.hcaptcha.com',
            'referer':              'https://newassets.hcaptcha.com/',
            'sec-ch-ua':            '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile':     '?0',
            'sec-ch-ua-platform':   '"Windows"',
            'sec-fetch-dest':       'empty',
            'sec-fetch-mode':       'cors',
            'sec-fetch-site':       'same-site',
            'user-agent':           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        r = self.session.post(f"https://hcaptcha.com/checksiteconfig?v=48ebaaf&host={self.host}&sitekey={self.sitekey}&sc=1&swa=1",headers=headers)
        return r.json()
    
    def e(self):
        headers = {
            'accept':               '*/*',
            'accept-encoding':      'gzip, deflate, br',
            'accept-language':      'en',
            'referer':              'https://newassets.hcaptcha.com/captcha/v1/48ebaaf/static/hcaptcha.html',
            'sec-ch-ua':            '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile':     '?0',
            'sec-ch-ua-platform':   '"Windows"',
            'sec-fetch-dest':       'empty',
            'sec-fetch-mode':       'cors',
            'sec-fetch-site':       'same-origin',
            'user-agent':           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        self.session.get("https://newassets.hcaptcha.com/i/b1686a2/e",headers=headers)
    
    def n(self,req):
        wd_opt = Options()
        wd_opt.headless = True
        wd_opt.add_argument("--no-sandbox")
        wd_opt.add_argument("--headless")
        wd_opt.add_argument("--disable-gpu")
        wd_opt.add_argument("--disable-software-rasterizer") 
        wd_opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        wd_opt.add_experimental_option('useAutomationExtension', False)
        wd_opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        wd = webdriver.Chrome(options=wd_opt, service_args=['--verbose'], service_log_path=None)
        atexit.register(lambda *_: wd.quit())

        with open("./hsw.js") as fp:
            wd.execute_script(fp.read() + "; window.hsw = hsw")

        hsw_time = 0
        hsw_last = None
        hsw_lock = threading.Lock()


        with hsw_lock:
            if time.time()-hsw_time > 5:
                proof = wd.execute_async_script(
                    "window.hsw(arguments[0]).then(arguments[1])",
                    req)
                hsw_last = proof
                hsw_time = time.time()
            else:
                proof = hsw_last + "".join(random.choices("ghijklmnopqrstuvwxyz", k=5))
        return proof
    
    def getcaptcha(self):
        data = {
            'v':            '48ebaaf',
            'sitekey':      self.sitekey,
            'host':         self.host,
            'hl':           'en',
            "motionData":   "{\"v\":1,\"topLevel\":{\"st\":1674396275720,\"sc\":{\"availWidth\":1280,\"availHeight\":720,\"width\":1280,\"height\":720,\"colorDepth\":24,\"pixelDepth\":24,\"top\":0,\"left\":0,\"availTop\":0,\"availLeft\":0,\"mozOrientation\":\"landscape-primary\",\"onmozorientationchange\":null},\"nv\":{\"permissions\":{},\"pdfViewerEnabled\":false,\"doNotTrack\":\"unspecified\",\"maxTouchPoints\":0,\"mediaCapabilities\":{},\"oscpu\":\"Windows NT 10.0; Win64; x64\",\"vendor\":\"\",\"vendorSub\":\"\",\"productSub\":\"20…20],[667,542,1674396277537],[665,542,1674396277554],[663,542,1674396277570],[659,542,1674396277586],[657,542,1674396277604],[656,542,1674396277637],[655,542,1674396277653],[655,540,1674396277770],[655,539,1674396277787],[655,536,1674396277804],[655,534,1674396277820]],\"mm-mp\":23.840909090909097},\"session\":[],\"widgetList\":[\"0t9y59de4qfi\"],\"widgetId\":\"0t9y59de4qfi\",\"href\":\"https://self.host/\",\"prev\":{\"escaped\":false,\"passed\":false,\"expiredChallenge\":false,\"expiredResponse\":false}}".replace("self.host",self.host),
            'n':            self.n(self.c["req"]),
            'c':            json.dumps(self.c,separators=(',',':')),
        }
        headers = {
            'accept':               'application/json',
            'accept-encoding':      'gzip, deflate, br',
            'accept-language':      'en',
            'content-length':       str(len(data)),
            'content-type':         'application/x-www-form-urlencoded',
            'origin':               'https://newassets.hcaptcha.com',
            'referer':              'https://newassets.hcaptcha.com/',
            'sec-ch-ua':            '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile':     '?0',
            'sec-ch-ua-platform':   '"Windows"',
            'sec-fetch-dest':       'empty',
            'sec-fetch-mode':       'cors',
            'sec-fetch-site':       'same-site',
            'user-agent':           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        return self.session.post(f"https://hcaptcha.com/getcaptcha/{self.sitekey}",headers=headers,data=urllib.parse.urlencode(data)).json()
        
    def download_cap(self):
        i = 1
        for captcha in self.cap["tasklist"]:
            url = captcha['datapoint_uri']
            # task = captcha['task_key']
            res = requests.get(url, stream = True)
            with open(f"./fotoz/{i}.png", 'wb') as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            i = i+1
    
    def solve(self,path,q):
        return [solve(f"{path}/{img}",q) for img in os.listdir(path)]
    
    def getmotion(self):
        ans = self.ans
        ans.append(True)
        start = int(str(time.time()).replace(".","")[:9]+"0000")
        real = [[77, 189, start+3443], [193, 192, start+4234], [331, 192, start+5223], [65, 326, start+6436], [199, 321, start+7197], [338, 318, start+8142], [73, 454, start+9364], [218, 454, start+10000+48], [335, 449, start+10000+891], [347, 556, start+10000+1703]]
        fr = [[77, 189, start+3496], [193, 192, start+4404], [331, 192, start+5328], [65, 326, start+6516], [199, 321, start+7320], [338, 318, start+8268], [73, 454, start+9481], [218, 454, start+10000+121], [335, 449, start+10000+1036], [347, 556, start+10000+1814]]
        clicks = []
        ups = []
        for i in range(len(ans)):
            if ans[i]:
                clicks.append(real[i])
                ups.append(fr[i])

        return {'st': start+566, 'dct': start+566, 'ku': [[9, start+2109]], 'ku-mp': 0, 'mm': [[0, 226, start+2886], [8, 222, start+2902], [17, 220, start+2918], [28, 217, start+2934], [40, 213, start+2950], [49, 209, start+2967], [57, 205, start+2984], [66, 201, start+3002], [76, 198, start+3018], [85, 195, start+3035], [93, 193, start+3051], [94, 191, start+3223], [90, 190, start+3240], [87, 190, start+3258], [85, 190, start+3279], [83, 190, start+3296], [80, 190, start+3315], [77, 189, start+3339], [78, 189, start+3508], [81, 189, start+3655], [83, 189, start+3671], [86, 189, start+3691], [89, 189, start+3708], [92, 191, start+3724], [99, 191, start+3740], [108, 191, start+3756], [119, 191, start+3772], [129, 191, start+3789], [139, 191, start+3806], [146, 191, start+3822], [151, 192, start+3840], [154, 192, start+3857], [158, 192, start+3874], [162, 192, start+3890], [166, 192, start+3908], [169, 192, start+3925], [173, 192, start+3942], [177, 192, start+3958], [180, 192, start+3982], [181, 192, start+4013], [183, 192, start+4029], [185, 192, start+4049], [187, 192, start+4071], [190, 192, start+4090], [193, 192, start+4187], [194, 192, start+4582], [198, 192, start+4599], [205, 192, start+4615], [216, 192, start+4631], [228, 192, start+4647], [239, 191, start+4663], [245, 191, start+4680], [251, 191, start+4697], [260, 191, start+4713], [274, 191, start+4729], [292, 191, start+4746], [306, 190, start+4763], [313, 189, start+4783], [314, 189, start+4852], [315, 189, start+4955], [316, 189, start+4974], [317, 189, start+4992], [319, 189, start+5014], [321, 189, start+5038], [324, 189, start+5063], [326, 190, start+5091], [328, 190, start+5130], [330, 191, start+5154], [330, 192, start+5411], [328, 192, start+5434], [325, 192, start+5452], [320, 193, start+5471], [314, 196, start+5488], [306, 201, start+5504], [293, 208, start+5520], [275, 219, start+5536], [253, 232, start+5552], [235, 242, start+5568], [221, 250, start+5584], [208, 258, start+5600], [198, 265, start+5616], [189, 271, start+5632], [178, 277, start+5648], [165, 282, start+5665], [155, 285, start+5682], [148, 287, start+5699], [141, 289, start+5717], [134, 293, start+5734], [124, 297, start+5751], [110, 303, start+5768], [94, 307, start+5785], [80, 309, start+5801], [68, 311, start+5817], [59, 313, start+5835], [54, 315, start+5853], [53, 315, start+5911], [54, 315, start+6013], [56, 317, start+6030], [59, 318, start+6051], [61, 319, start+6068], [62, 320, start+6088], [63, 321, start+6112], [64, 323, start+6131], [64, 325, start+6152], [65, 326, start+6170], [66, 326, start+6526], [67, 324, start+6547], [68, 323, start+6571], [71, 322, start+6592], [74, 321, start+6608], [77, 320, start+6624], [81, 319, start+6641], [88, 319, start+6659], [99, 318, start+6675], [116, 316, start+6691], [134, 315, start+6707], [153, 314, start+6723], [167, 312, start+6739], [174, 312, start+6755], [175, 312, start+6796], [178, 312, start+6813], [184, 313, start+6829], [193, 314, start+6847], [200, 315, start+6864], [204, 316, start+6881], [206, 316, start+6900], [208, 317, start+6918], [211, 318, start+6940], [212, 319, start+6963], [211, 319, start+7027], [208, 320, start+7046], [205, 320, start+7067], [202, 320, start+7085], [200, 321, start+7102], [199, 321, start+7131], [200, 321, start+7427], [203, 321, start+7452], [207, 321, start+7471], [214, 321, start+7489], [224, 321, start+7505], [237, 320, start+7521], [250, 319, start+7537], [266, 318, start+7553], [279, 317, start+7569], [288, 316, start+7585], [294, 315, start+7602], [297, 315, start+7620], [298, 314, start+7654], [300, 314, start+7670], [304, 314, start+7687], [310, 314, start+7703], [316, 314, start+7720], [321, 314, start+7739], [325, 314, start+7755], [330, 314, start+7771], [335, 313, start+7788], [340, 313, start+7808], [343, 313, start+7830], [345, 313, start+7846], [347, 313, start+7864], [347, 313, start+7972], [345, 314, start+7988], [343, 314, start+8009], [342, 316, start+8031], [341, 317, start+8047], [339, 317, start+8066], [338, 318, start+8126], [338, 317, start+8313], [339, 317, start+8358], [338, 317, start+8485], [334, 317, start+8501], [327, 321, start+8517], [319, 326, start+8533], [310, 332, start+8550], [297, 340, start+8566], [275, 352, start+8582], [248, 363, start+8598], [222, 374, start+8614], [198, 385, start+8630], [179, 395, start+8646], [168, 403, start+8663], [161, 407, start+8680], [159, 409, start+8697], [158, 411, start+8717], [152, 413, start+8736], [147, 415, start+8753], [139, 417, start+8770], [131, 418, start+8786], [124, 420, start+8803], [119, 422, start+8823], [117, 423, start+8841], [115, 425, start+8857], [109, 426, start+8874], [105, 428, start+8890], [100, 430, start+8907], [94, 433, start+8923], [88, 436, start+8939], [84, 438, start+8956], [82, 439, start+8981], [80, 440, start+9000], [78, 442, start+9016], [76, 443, start+9038], [75, 444, start+9059], [75, 445, start+9188], [75, 447, start+9212], [74, 448, start+9229], [74, 450, start+9248], [73, 452, start+9272], [73, 454, start+9296], [73, 453, start+9506], [75, 452, start+9531], [77, 451, start+9551], [79, 450, start+9570], [83, 449, start+9590], [87, 448, start+9606], [93, 448, start+9624], [101, 447, start+9641], [115, 446, start+9657], [130, 446, start+9673], [145, 446, start+9689], [158, 446, start+9706], [167, 446, start+9724], [170, 447, start+9742], [173, 448, start+9759], [177, 450, start+9778], [182, 450, start+9798], [187, 450, start+9815], [193, 451, start+9832], [199, 451, start+9849], [206, 451, start+9867], [211, 452, start+9883], [216, 453, start+9901], [219, 454, start+10000+379], [221, 454, start+10000+399], [223, 454, start+10000+416], [229, 453, start+10000+432], [240, 453, start+10000+448], [253, 453, start+10000+464], [263, 453, start+10000+480], [273, 452, start+10000+496], [281, 452, start+10000+512], [286, 452, start+10000+528], [289, 452, start+10000+548], [293, 450, start+10000+565], [297, 450, start+10000+583], [300, 449, start+10000+608], [302, 449, start+10000+634], [305, 449, start+10000+653], [307, 449, start+10000+669], [309, 449, start+10000+693], [313, 449, start+10000+710], [319, 449, start+10000+726], [324, 449, start+10000+742], [328, 449, start+10000+762], [331, 449, start+10000+783], [333, 449, start+10000+804], [334, 449, start+10000+842], [335, 449, start+10000+889], [334, 449, start+10000+1075], [334, 450, start+10000+1099], [333, 451, start+10000+1118], [333, 454, start+10000+1136], [333, 457, start+10000+1154], [333, 461, start+10000+1170], [335, 466, start+10000+1189], [336, 471, start+10000+1207], [337, 477, start+10000+1224], [339, 485, start+10000+1241], [340, 494, start+10000+1258], [342, 503, start+10000+1274], [343, 509, start+10000+1290], [344, 515, start+10000+1307], [345, 520, start+10000+1325], [346, 525, start+10000+1341], [346, 531, start+10000+1360], [347, 535, start+10000+1377], [347, 539, start+10000+1397], [347, 543, start+10000+1420], [347, 545, start+10000+1436], [348, 547, start+10000+1483], [348, 549, start+10000+1508], [348, 551, start+10000+1526], [348, 553, start+10000+1546], [348, 555, start+10000+1615], [348, 556, start+10000+1633]], 'mm-mp': 5.28580060422961, 'md': clicks, 'md-mp': 917.7777777777778, 'mu': ups, 'mu-mp': 924.2222222222222, 'topLevel': {'st': start-10000+7843, 'sc': {'availWidth': 1920, 'availHeight': 1032, 'width': 1920, 'height': 1080, 'colorDepth': 24, 'pixelDepth': 24, 'availLeft': 0, 'availTop': 0, 'onchange': None, 'isExtended': False}, 'nv': {'vendorSub': '', 'productSub': '20030107', 'vendor': 'Google Inc.', 'maxTouchPoints': 0, 'scheduling': {}, 'userActivation': {}, 'doNotTrack': None, 'geolocation': {}, 'connection': {}, 'pdfViewerEnabled': True, 'webkitTemporaryStorage': {}, 'hardwareConcurrency': 16, 'cookieEnabled': True, 'appCodeName': 'Mozilla', 'appName': 'Netscape', 'appVersion': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 'platform': 'Win32', 'product': 'Gecko', 'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 'language': 'en', 'languages': ['en'], 'onLine': True, 'webdriver': False, 'bluetooth': {}, 'clipboard': {}, 'credentials': {}, 'keyboard': {}, 'managed': {}, 'mediaDevices': {}, 'storage': {}, 'serviceWorker': {}, 'virtualKeyboard': {}, 'wakeLock': {}, 'deviceMemory': 8, 'ink': {}, 'hid': {}, 'locks': {}, 'mediaCapabilities': {}, 'mediaSession': {}, 'permissions': {}, 'presentation': {}, 'serial': {}, 'usb': {}, 'windowControlsOverlay': {}, 'xr': {}, 'userAgentData': {'brands': [{'brand': 'Not_A Brand', 'version': '99'}, {'brand': 'Google Chrome', 'version': '109'}, {'brand': 'Chromium', 'version': '109'}], 'mobile': False, 'platform': 'Windows'}, 'plugins': ['internal-pdf-viewer', 'internal-pdf-viewer', 'internal-pdf-viewer', 'internal-pdf-viewer', 'internal-pdf-viewer']}, 'dr': '', 'inv': False, 'exec': False, 'wn': [], 'wn-mp': 0, 'xy': [], 'xy-mp': 0, 'mm': [[856, 485, start-10000+7071], [825, 485, start-10000+7087], [797, 486, start-10000+7103], [772, 488, start-10000+7119], [751, 490, start-10000+7135], [732, 492, start-10000+7151], [719, 494, start-10000+7167], [711, 495, start-10000+7183], [706, 496, start-10000+7200], [702, 497, start-10000+7219], [701, 498, start-10000+7518], [707, 498, start-10000+7534], [717, 496, start-10000+7550], [725, 494, start-10000+7566], [732, 493, start-10000+7583], [733, 491, start-10000+7697], [733, 487, start-10000+7720], [656, 364, start-10000+9162], [756, 402, start-10000+9178], [761, 453, start+2015], [762, 453, start+2544], [769, 453, start+2565], [769, 452, start+2600], [769, 450, start+2622], [769, 448, start+2638], [769, 445, start+2657], [771, 443, start+2673], [772, 442, start+2702], [772, 440, start+2724], [774, 438, start+2743], [777, 435, start+2762], [781, 431, start+2779], [789, 426, start+2796], [799, 421, start+2812], [812, 415, start+2828], [826, 408, start+2844], [839, 401, start+2860], [850, 395, start+2876]], 'mm-mp': 16.567226890756277, 'md': [[700, 498, start-10000+7297]], 'md-mp': 10287, 'mu': [[700, 498, start-10000+7403]], 'mu-mp': 10292}, 'v': 1}
    
    def checkcaptcha(self):
        # console.log(dict(zip([captcha["task_key"] for captcha in self.cap["tasklist"]],self.ans)))
        payload = {
                "v": "48ebaaf",
                "job_mode": "image_label_binary",
                "answers": json.dumps(dict(zip([captcha["task_key"] for captcha in self.cap["tasklist"]],self.ans)),separators=(',',':')),
                    "serverdomain": self.host,
                    "sitekey": self.sitekey,
                    "motionData":json.dumps(self.getmotion(),separators=(',',':')),
                    "n": self.n(self.c["req"]),
                    "c": json.dumps(self.c,separators=(',',':'))
            }
        headers = {
            'accept':               '*/*',
            'accept-encoding':      'gzip, deflate, br',
            'accept-language':      'en',
            'content-length':       str(len(payload)),
            'content-type':         'application/json;charset=UTF-8',
            'origin':               'https://newassets.hcaptcha.com',
            'referer':              'https://newassets.hcaptcha.com/',
            'sec-ch-ua':            '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile':     '?0',
            'sec-ch-ua-platform':   '"Windows"',
            'sec-fetch-dest':       'empty',
            'sec-fetch-mode':       'cors',
            'sec-fetch-site':       'same-site',
            'user-agent':           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        return self.session.post(f"https://hcaptcha.com/checkcaptcha/{self.sitekey}/{self.cap['key']}",json=payload,headers=headers)

hcap(sitekey="4c672d35-0701-42b2-88c3-78380b0db560",host="discord.com")
