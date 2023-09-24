from bs4 import BeautifulSoup
class ZhihuAnalyser:

    def recordAndDiscover(response, qid):
        dataStr = response.text
        bs = BeautifulSoup(dataStr, 'html.parser')
        summary = bs.select(".lemma-summary")
        title = bs.select(".J-lemma-title")
        titleStr = ""
        if len(title) > 0:
            h1 = title[0].select("h1")
            if len(h1) > 0:
                titleStr = stripHtmlTag(h1[0].text)
        if len(summary) > 0:
            paragraphs = summary[0].select('.para')
            SummaryList = []
            for p in paragraphs:
                SummaryList.append(stripHtmlTag(p.text))
                newLink = discoverLink(p)
                for l in newLink:
                    newQid(l)
            joinedStr = convertNewLineAndTable('[SEP]'.join([p.text for p in paragraphs]))
            outputLine = titleStr + "\t" + joinedStr
            print(outputLine)
            record(outputLine)
        # state saving
        if not scrapedQid.__contains__(qid):
            scrapedQid.add(qid)

        return False, True

    pass