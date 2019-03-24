import dropbox
import os.path

TOKEN = "(アクセストークン)"

class Dropbox:
    def __init__(self, user_name, sns):
        self.user_name = user_name
        self.sns = sns
        self.dbx = dropbox.Dropbox(TOKEN)
        self.dbx.users_get_current_account()
    
    # 保存ディレクトリ作成
    def makeDropboxFolder(self):
        # 親ディレクトリ作成
        is_parent_directory_exists = False
        for entry in self.dbx.files_list_folder('').entries:
            if (entry.name == self.user_name):
                is_parent_directory_exists = True
                break
        if (is_parent_directory_exists == False):
            self.dbx.files_create_folder('/' + self.user_name)

        # 各SNSディレクトリ作成
        is_sns_directory_exists = False
        for entry in self.dbx.files_list_folder('/' + self.user_name).entries:
            if (entry.name == self.sns):
                is_sns_directory_exists = True
                break
        if (is_sns_directory_exists == False):
                self.dbx.files_create_folder('/' + self.user_name + '/' + self.sns)

    # 写真アップロード
    def uploadPicture(self, local_image_path):
        with open(local_image_path, "rb" ) as f:
            self.dbx.files_upload(f.read(), '/' + self.user_name + '/' + self.sns + '/' + os.path.basename(local_image_path))

