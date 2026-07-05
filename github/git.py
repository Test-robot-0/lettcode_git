from github.app import gen_readme, root_gen_readme, upload_file
import database.repository as repository

def git_run(current_id):

    difficulty, frontend_id, title_slug, language_verbose, code = repository.get_path(current_id)
    solution_path = f"{difficulty}/{frontend_id:04}_{title_slug}/Solution{language_verbose}"
    readme_path   = f"{difficulty}/{frontend_id:04}_{title_slug}/README.md"

    status = repository.get_status(current_id)
    if  status == 4: 
        readme_status = upload_file(readme_path, gen_readme(current_id), f"Added README for {frontend_id:04}_{title_slug}", "readme", current_id)
        print(f"(5/7) Done gen_readme: {readme_status}")

    status = repository.get_status(current_id)
    if status == 5:
        code_status = upload_file(solution_path, code, f"Added Solution for {frontend_id:04}_{title_slug}", "solution", current_id)
        print(f"(6/7) Done code: {code_status}")
    
    status = repository.get_status(current_id)
    if status == 6:
        try:
            repository.update_status_7(current_id)
            root_readme_status = upload_file("README.md", root_gen_readme(current_id), f"Updated README", "root_readme", current_id)
            print(f"(7/7) Done root_gen_readme: {root_readme_status}")
        except :
            repository.update_status_6(current_id)

    status = repository.get_status(current_id)
    if status == 7:
        print("status", status)
        print("Congratulations...")

