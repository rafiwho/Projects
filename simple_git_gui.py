import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, simpledialog
import git

class GitGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple Git GUI")
        master.geometry("900x700")
        master.configure(bg="#1c1c1c")

        self.repo_path = ""
        self.repo = None
        self.clone_type = tk.StringVar(value="SSH")

        self.title_label = tk.Label(master, text="Simple Git GUI", bg="#1c1c1c", fg="#00ff00", font=("Courier New", 16, "bold"))
        self.title_label.pack(pady=10)

        self.label = tk.Label(master, text="Select a Git Repository:", bg="#1c1c1c", fg="#ffffff", font=("Courier New", 12))
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select Repository", command=self.select_repo, bg="#ffffff", fg="#000000", font=("Courier New", 10))
        self.select_button.pack(pady=5)

        self.clone_type_label = tk.Label(master, text="Clone Repository Using:", bg="#1c1c1c", fg="#ffffff", font=("Courier New", 12))
        self.clone_type_label.pack(pady=10)

        self.ssh_radio = tk.Radiobutton(master, text="SSH", variable=self.clone_type, value="SSH", bg="#1c1c1c", fg="#00ff00", font=("Courier New", 10), selectcolor="#1c1c1c")
        self.ssh_radio.pack()

        self.https_radio = tk.Radiobutton(master, text="HTTPS", variable=self.clone_type, value="HTTPS", bg="#1c1c1c", fg="#00ff00", font=("Courier New", 10), selectcolor="#1c1c1c")
        self.https_radio.pack()

        self.clone_button = tk.Button(master, text="Clone Repository", command=self.clone_repo, bg="#ffffff", fg="#000000", font=("Courier New", 10))
        self.clone_button.pack(pady=5)

        self.commit_list_label = tk.Label(master, text="Commit History:", bg="#1c1c1c", fg="#ffffff", font=("Courier New", 12))
        self.commit_list_label.pack(pady=10)

        self.commit_listbox = Listbox(master, width=80, bg="#2d2d2d", fg="#00ff00", font=("Courier New", 10))
        self.commit_listbox.pack(pady=5)

        self.stage_button = tk.Button(master, text="Stage Changes", command=self.stage_changes, state=tk.DISABLED, bg="#ffffff", fg="#000000", font=("Courier New", 10))
        self.stage_button.pack(pady=5)

        self.commit_button = tk.Button(master, text="Commit Changes", command=self.commit_changes, state=tk.DISABLED, bg="#ffffff", fg="#000000", font=("Courier New", 10))
        self.commit_button.pack(pady=5)

        self.push_button = tk.Button(master, text="Push Changes", command=self.push_changes, state=tk.DISABLED, bg="#ffffff", fg="#000000", font=("Courier New", 10))
        self.push_button.pack(pady=5)

        self.pull_button = tk.Button(master, text="Pull Changes", command=self.pull_changes, state=tk.DISABLED, bg="#ffffff", fg="#000000", font=("Courier New", 10))
        self.pull_button.pack(pady=5)

    def select_repo(self):
        self.repo_path = filedialog.askdirectory()
        if self.repo_path and os.path.isdir(self.repo_path):
            self.repo = git.Repo(self.repo_path)
            self.update_commit_list()
            self.stage_button.config(state=tk.NORMAL)
            self.commit_button.config(state=tk.NORMAL)
            self.push_button.config(state=tk.NORMAL)
            self.pull_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Please select a valid Git repository.")

    def update_commit_list(self):
        self.commit_listbox.delete(0, tk.END)
        for commit in self.repo.iter_commits():
            self.commit_listbox.insert(tk.END, f"{commit.hexsha[:7]} - {commit.message.strip()}")

    def stage_changes(self):
        try:
            self.repo.git.add(A=True)
            messagebox.showinfo("Success", "All changes staged.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stage changes: {str(e)}")

    def commit_changes(self):
        commit_message = simpledialog.askstring("Commit Changes", "Enter commit message:")
        if not commit_message:
            messagebox.showerror("Error", "Commit message cannot be empty.")
            return
        try:
            self.repo.index.commit(commit_message)
            messagebox.showinfo("Success", "Changes committed.")
            self.update_commit_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to commit changes: {str(e)}")

    def push_changes(self):
        try:
            self.repo.git.push()
            messagebox.showinfo("Success", "Changes pushed to remote repository.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to push changes: {str(e)}")

    def pull_changes(self):
        try:
            self.repo.git.pull()
            messagebox.showinfo("Success", "Changes pulled from remote repository.")
            self.update_commit_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to pull changes: {str(e)}")

    def clone_repo(self):
        if self.clone_type.get() == "SSH":
            repo_url = simpledialog.askstring("Clone Repository", "Enter the Git SSH URL of the repository (e.g., git@github.com:user/repository.git):")
        else:
            repo_url = simpledialog.askstring("Clone Repository", "Enter the Git HTTPS URL of the repository:")

        if repo_url:
            target_dir = filedialog.askdirectory(title="Select Target Directory")
            if target_dir:
                try:
                    git.Repo.clone_from(repo_url, os.path.join(target_dir, os.path.basename(repo_url)))
                    messagebox.showinfo("Success", f"Repository cloned to {target_dir}.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to clone repository: {str(e)}")
            else:
                messagebox.showerror("Error", "Please select a valid target directory.")
        else:
            messagebox.showerror("Error", "Please enter a valid Git URL.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GitGUI(root)
    root.mainloop()
