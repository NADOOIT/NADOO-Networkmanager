import json
import os
import shutil
import time
import git
import argparse

# Get the absolute path of the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, "src")
# Files src paths
user_data_file = os.path.join(src_dir, "data/db/benutzer_data.json")
user_presentation_data_file = os.path.join(src_dir, "data/db/benutzer_kurzpraesentation_data.json")

# Ensure the necessary directories exist
data_directory = os.path.join(src_dir, "data", "db")
backup_directory = os.path.join(script_dir, "backup")

# Presentation or Image backup paths
media_file_backup_dir = os.path.join(backup_directory, "media_file")

for directory in [data_directory, backup_directory, media_file_backup_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")


def read_file(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        return json.load(file)


def write_to_file(file_path: str, content: str) -> None:
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)


def get_media_files_paths(file):
    media_file_paths = []
    content = read_file(file)

    if 'benutzer' in content:
        for user in content['benutzer']:
            media_file_paths.append(user['foto'])
    elif 'benutzer_kurzpraesentation' in content:
        for pre in content['benutzer_kurzpraesentation']:
            media_file_paths.append(pre['folien_path'])
    return media_file_paths


# Backup the data before deleting it
def backup_data():
    try:
        files = [user_data_file, user_presentation_data_file]

        for file in files:
            print(f"Backing up {os.path.basename(file)}...")
            try:
                media_files_paths = get_media_files_paths(file)
                shutil.copy(file, os.path.join(backup_directory, os.path.basename(file)))
                print(f"Backing up media files from: {os.path.basename(file)}...")
                for media_file_path in media_files_paths:
                    media_file_path = os.path.join(src_dir, media_file_path)
                    shutil.copy(media_file_path, media_file_backup_dir)
                    print(f"Successfully backed up {media_file_path}")
                print(f"Successfully backed up {os.path.basename(file)}")
            except Exception as e:
                raise Exception(f"Error during backup: {e}")

    except Exception as e:
        print(f"Error during backup: {e}")


# Delete the user data, presentation data, and associated media files
def delete_user_data():
    try:
        print(f"Deleting data in {user_data_file}...")
        data = read_file(user_data_file)
        if 'benutzer' in data:
            for user in data['benutzer']:
                foto_path = os.path.join(src_dir, user['foto'])
                if os.path.exists(foto_path):
                    os.remove(foto_path)
                    print(f"Deleted photo: {foto_path}")
            data['benutzer'] = []
        write_to_file(user_data_file, data)
        print(f"Successfully deleted data in {user_data_file}")
    except Exception as e:
        print(f"Error deleting data in {user_data_file}: {e}")


def delete_user_presentation_data():
    try:
        print(f"Deleting data in {user_presentation_data_file}...")
        data = read_file(user_presentation_data_file)
        if 'benutzer_kurzpraesentation' in data:
            for pre in data['benutzer_kurzpraesentation']:
                folien_path = os.path.join(src_dir, pre['folien_path'])
                if os.path.exists(folien_path):
                    os.remove(folien_path)
                    print(f"Deleted file: {folien_path}")
            data['benutzer_kurzpraesentation'] = []
        write_to_file(user_presentation_data_file, data)
        print(f"Successfully deleted data in {user_presentation_data_file}")
    except Exception as e:
        print(f"Error deleting data in {user_presentation_data_file}: {e}")


# Commit and push the changes to the remote repo
def commit_and_push_changes(commit_message):
    print("Committing and pushing changes to the remote repository...")
    try:
        repo = git.Repo(search_parent_directories=True)
        repo.git.add(A=True)  # Add all changes
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')

        # Check if the current branch has an upstream branch
        current_branch = repo.active_branch
        if current_branch.tracking_branch() is None:
            print(f"Setting upstream for the branch {current_branch}")
            origin.push(refspec=f"{current_branch}:{current_branch}", set_upstream=True)
        else:
            origin.push()
        print("Changes committed and pushed.")
    except Exception as e:
        print(f"Error during commit and push: {e}")


# Restore the sensitive data
def restore_data():
    try:
        # Restore the data from the backup
        user_data_file_backup = os.path.join(backup_directory, os.path.basename(user_data_file))
        user_presentation_data_file_backup = os.path.join(backup_directory,
                                                          os.path.basename(user_presentation_data_file))

        backup_files = [user_data_file_backup, user_presentation_data_file_backup]

        for file in backup_files:
            print(f"Restoring {os.path.basename(file)}...")
            try:
                media_file_paths = get_media_files_paths(file)
                dest_file_path = os.path.join(data_directory, os.path.basename(file))
                shutil.copy(file, dest_file_path)
                print(f"Restoring media files from: {os.path.basename(file)}...")
                for media_file_path in media_file_paths:
                    media_file_path_backup = os.path.join(media_file_backup_dir, os.path.basename(media_file_path))
                    dest_path = os.path.join(src_dir, "resources", "images",
                                             "benutzer") if "foto" in media_file_path else os.path.join(src_dir,
                                                                                                        "resources",
                                                                                                        "vorlage",
                                                                                                        "kurzpraesentationen")
                    dest_file_path = os.path.join(dest_path, os.path.basename(media_file_path))
                    print(f"Restoring {media_file_path_backup} to {dest_file_path}")
                    shutil.copy(media_file_path_backup, dest_file_path)
                    print(f"Successfully restored {dest_file_path}")
                print(f"Successfully restored {os.path.basename(file)}")
            except Exception as e:
                raise Exception(f"Error during restoring: {e}")

    except Exception as e:
        print(f"Error during restoring: {e}")


# Main script execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Delete sensitive data and commit changes to Git repository.')
    parser.add_argument('commit_message', type=str, help='Commit message for the changes.')
    args = parser.parse_args()

    # Backup data
    backup_data()

    time.sleep(5)
    # Delete sensitive data
    delete_user_data()
    delete_user_presentation_data()

    # Commit and push changes
    commit_and_push_changes(args.commit_message)

    time.sleep(5)
    # Restore data
    restore_data()

    # shutil.rmtree(backup_directory)

    print("Script execution completed.")
