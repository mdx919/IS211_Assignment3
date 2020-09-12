import csv, re, urllib.request, argparse, sys


def downloadData(url):
    # uncomment below code to make url based csv file to work
    try:
        response = urllib.request.urlopen(url)
        lines = [l.decode('utf-8') for l in response.readlines()]
        csvData = csv.reader(lines, delimiter=',', quotechar='"')
        webData = processData(csvData)
        print('Image requests account for {}% of all requests.'.format(getImagePercentage(webData)))
        print('Most popular broweser is {}.'.format(getPopularBrowser(webData).capitalize()))
        hourHits = getHourlyHits(webData)

        if hourHits:
            for key in hourHits:
                print("Hour {} has {} hits.".format(key, hourHits[key]))

    except ValueError:
        print('Error processing the CSV file')
        sys.exit()

    # uncomment below code to make local file to work
    # try:
    #     with open('data.csv', newline='') as csvfile:
    #         csvData = csv.reader(csvfile, delimiter=',', quotechar='"')
    #         webData = processData(csvData)
    #         print('Image requests account for {}% of all requests.'.format(getImagePercentage(webData)))
    #         print('Most popular broweser is {}.'.format(getPopularBrowser(webData).capitalize()))
    #         hourHits = getHourlyHits(webData)
    #
    #         if hourHits:
    #             for key in hourHits:
    #                 print("Hour {} has {} hits.".format(key, hourHits[key]))
    #
    # except ValueError:
    #     print('Error processing the CSV file')
    #     sys.exit()

def getImagePercentage(data):
    count = 0
    for i in data:
        match = re.findall(r"\S+\.jpg|.png|.gif", i['file'].lower())
        if match:
            count += 1
    percentage = (count / len(data)) * 100
    return percentage

def getPopularBrowser(data):
    browsers = dict(firefox=0, chrome = 0, safari = 0, internetExplorer= 0)

    for i in data:
        match = re.findall("firefox|chrome|internet explorer|safari", i['browser'].lower())
        if match:
            for b in match:
                if b == 'firefox':
                    browsers['firefox'] += 1
                elif b == 'safari':
                    browsers['safari'] += 1
                elif b == 'chrome':
                    browsers['chrome'] += 1
                elif b == 'internet explorer':
                    browsers['internetExplorer'] += 1
    browserName = ''
    maxNum = 0
    for key in browsers:
        if browsers[key] > maxNum:
            maxNum = browsers[key]
            browserName = key
    return browserName

def getHourlyHits(data):
    timesHit = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    for i in data:
        if i['timeStamp'][11:13] == '00':
            timesHit[0] += 1
        else:
            timesHit[int(i['timeStamp'][11:13].strip('0'))] += 1
    return timesHit



def processData(data):
    result = []
    for i, row in enumerate(data):
        eachRequest = {'file': row[0], 'timeStamp': row[1], 'browser': row[2], 'status': row[3], 'size': row[4]}
        result.append(eachRequest)
    return result


parser = argparse.ArgumentParser()
parser.add_argument("--url")
args = parser.parse_args()
if len(sys.argv) < 2 or sys.argv[1] != '--url':
    sys.exit()
elif len(sys.argv) > 1 and sys.argv[1] == '--url':
    downloadData(sys.argv[2])
