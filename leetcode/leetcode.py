import requests
import json
import config
import database.repository as repository



def set_problem_info(length):

    cookies = config.COOKIES

    json_data = {
        'query': '\n    query userProgressQuestionList($filters: UserProgressQuestionListInput) {\n  userProgressQuestionList(filters: $filters) {\n    totalNum\n    questions {\n      translatedTitle\n      frontendId\n      title\n      titleSlug\n      difficulty\n      lastSubmittedAt\n      numSubmitted\n      questionStatus\n      lastResult\n      topicTags {\n        name\n        nameTranslated\n        slug\n      }\n    }\n  }\n}\n    ',
        'variables': {
            'filters': {
                'questionStatus': 'SOLVED',
                'skip': 0,
                'limit': 50,
                'sortOrder': 'DESCENDING',
                'sortField': 'NUM_SUBMITTED',
            },
        },
        'operationName': 'userProgressQuestionList',
    }

    response = requests.post('https://leetcode.com/graphql/', cookies=cookies, json=json_data)

    if length < response.json()["data"]["userProgressQuestionList"]["totalNum"]:
        data = response.json()["data"]["userProgressQuestionList"]["questions"]

        print("Exiqueted_leetcode")
        for i in range(0, len(data)):
            
            repository.insert_info_solutions(data[i]["frontendId"], data[i]["title"], data[i]["titleSlug"], data[i]["difficulty"].capitalize(), json.dumps(data[i]["topicTags"]))
            repository.update_status_1() 
    
    repository.commit()
        
    print("\n(1/7) Done with the problems info")




def set_submission_info(current_id, title_slug):

    cookies = config.COOKIES

    json_data = {
        'query': '\n    query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!, $lang: Int, $status: Int) {\n  questionSubmissionList(\n    offset: $offset\n    limit: $limit\n    lastKey: $lastKey\n    questionSlug: $questionSlug\n    lang: $lang\n    status: $status\n  ) {\n    lastKey\n    hasNext\n    submissions {\n      id\n      title\n      titleSlug\n      status\n      statusDisplay\n      lang\n      langName\n      runtime\n      timestamp\n      url\n      isPending\n      memory\n      hasNotes\n      notes\n      flagType\n      frontendId\n      topicTags {\n        id\n      }\n    }\n  }\n}\n    ',
        'variables': {
            'questionSlug': title_slug, # 'two-sum'
            'offset': 0,
            'limit': 20,
            'lastKey': None,
        },
        'operationName': 'submissionList',
    }


    response = requests.post('https://leetcode.com/graphql/', cookies=cookies, json=json_data)
    data = response.json()["data"]["questionSubmissionList"]["submissions"]

    id = 0
    iteration = 0

    if len(data) > 1:
        min_ = 10000000    

        for i in range(0, len(data)):
            
            if data[i]["statusDisplay"] == "Accepted":
                num = data[i]["runtime"]
                new = int(num.replace(" ms", ""))

                if min_ > new:
                    min_ = new
                    id = data[i]["id"]
                    iteration = i
    
    else:
        id = data[0]["id"]
    
    language_name = config.EXTENSIONS.get(data[iteration]["lang"].lower(), ".txt")

    repository.update_submisstion_solutions(id, language_name, data[iteration]["langName"], data[iteration]["memory"], data[iteration]["runtime"], current_id)
    repository.commit()

    print("(3/7) Done with the submission info")


def set_code(current_id, question_id):

    cookies = config.COOKIES

    json_data = {
        'query': '\n    query submissionDetails($submissionId: Int!) {\n  submissionDetails(submissionId: $submissionId) {\n    runtime\n    runtimeDisplay\n    runtimePercentile\n    runtimeDistribution\n    memory\n    memoryDisplay\n    memoryPercentile\n    memoryDistribution\n    code\n    timestamp\n    statusCode\n    aiJudgeMessage\n    isCompiledLang\n    aiRecheckSubmitted\n    user {\n      username\n      profile {\n        realName\n        userAvatar\n      }\n    }\n    lang {\n      name\n      verboseName\n    }\n    question {\n      questionId\n      titleSlug\n      hasFrontendPreview\n    }\n    notes\n    flagType\n    topicTags {\n      tagId\n      slug\n      name\n    }\n    runtimeError\n    compileError\n    lastTestcase\n    codeOutput\n    expectedOutput\n    totalCorrect\n    totalTestcases\n    fullCodeOutput\n    testDescriptions\n    testBodies\n    testInfo\n    stdOutput\n  }\n}\n    ',
        'variables': {
            'submissionId': question_id, #1598230880
        },
        'operationName': 'submissionDetails',
    }


    response = requests.post('https://leetcode.com/graphql/', cookies=cookies, json=json_data)

    data = response.json()["data"]["submissionDetails"]
    repository.update_code_solutions(data["code"], current_id)
    repository.commit()

    print("(4/7) Done with the code")


