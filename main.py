import config
import database.schema
import database.repository as repository
from leetcode.leetcode import set_problem_info, set_submission_info, set_code
from github.git import git_run
from leetcode.question import get_question


cookies = config.COOKIES
length = repository.get_size_id()


get_question("asteroid-collision", 1)
print("----"*50)

set_problem_info(length)

current_id, title_slug, status = repository.get_submission_info()
if status == 1:
    set_submission_info(current_id, title_slug)


question_id, status = repository.get_code_info(current_id)
if status == 2:
    set_code(current_id, question_id)

status = repository.get_status(current_id)
if status == 3:
    get_question(title_slug, current_id)

status = repository.get_status(current_id)
if  status >= 4:
    git_run(current_id)

repository.commit()


#git_run(repository.new_current_id())
#
#print(f"----- Done {title_slug}")




#get_question(title_slug, conn)
#
#from old_git import push_github
#
#push_github()
