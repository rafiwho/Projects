import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, simpledialog
import git

# Main class for Git GUI application
class GitGUI:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        master.title("Simple Git GUI")
        master.geometry("900x700")
        master.configure(bg="#1c1c1c")  # Dark background

        self.repo_path = ""
        self.repo = None
        self.clone_type = tk.StringVar(value="SSH")  # Variable for choosing between SSH and HTTPS

        # Title label setup
        self.title_label = tk.Label(master, text="Simple Git GUI", bg="#1c1c1c", fg="#00ff00", font=("Courier New", 16, "bold"))
        self.title_label.pack(pady=10)

        # Label for selecting Git repository
        self.label = tk.Label(master, text="Select a Git Repository:", bg="#1c1c1c", fg="#ffffff", font=("Courier New", 12))
        self.label.pack(pady=10)

        # Button for selecting a repository directory
        self.select_button = tk.Button(master, text="Select Repository", command=self.select_repo, bg="#007700", fg="#ffffff", font=("Courier New", 10))
        self.select_button.pack(pady=5)

        # Clone repository option label and radio buttons
        self.clone_type_label = tk.Label(master, text="Clone Repository Using:", bg="#1c1c1c", fg="#ffffff", font=("Courier New", 12))
        self.clone_type_label.pack(pady=10)

        # Radio button for SSH option
        self.ssh_radio = tk.Radiobutton(master, text="SSH", variable=self.clone_type, value="SSH", bg="#1c1c1c", fg="#00ff00", font=("Courier New", 10), selectcolor="#2d2d2d")
        self.ssh_radio.pack()

        # Radio button for HTTPS option
        self.https_radio = tk.Radiobutton(master, text="HTTPS", variable=self.clone_type, value="HTTPS", bg="#1c1c1c", fg="#00ff00", font=("Courier New", 10), selectcolor="#2d2d2d")
        self.https_radio.pack()

        # Button to trigger the clone repository process
        self.clone_button = tk.Button(master, text="Clone Repository", command=self.clone_repo, bg="#007700", fg="#ffffff", font=("Courier New", 10))
        self.clone_button.pack(pady=5)

        # Label and listbox for displaying commit history
        self.commit_list_label = tk.Label(master, text="Commit History:", bg="#1c1c1c", fg="#ffffff", font=("Courier New", 12))
        self.commit_list_label.pack(pady=10)

        # Listbox to show commit history from the selected repository
        self.commit_listbox = Listbox(master, width=80, bg="#2d2d2d", fg="#00ff00", font=("Courier New", 10))
        self.commit_listbox.pack(pady=5)

        # Buttons for Git operations: stage, commit, push, and pull
        self.stage_button = tk.Button(master, text="Stage Changes", command=self.stage_changes, state=tk.DISABLED, bg="#007700", fg="#ffffff", font=("Courier New", 10))
        self.stage_button.pack(pady=5)

        self.commit_button = tk.Button(master, text="Commit Changes", command=self.commit_changes, state=tk.DISABLED, bg="#007700", fg="#ffffff", font=("Courier New", 10))
        self.commit_button.pack(pady=5)

        self.push_button = tk.Button(master, text="Push Changes", command=self.push_changes, state=tk.DISABLED, bg="#007700", fg="#ffffff", font=("Courier New", 10))
        self.push_button.pack(pady=5)

        self.pull_button = tk.Button(master, text="Pull Changes", command=self.pull_changes, state=tk.DISABLED, bg="#007700", fg="#ffffff", font=("Courier New", 10))
        self.pull_button.pack(pady=5)

    # Method to select a repository directory
    def select_repo(self):
        # Open a directory selection dialog and assign the selected path
        self.repo_path = filedialog.askdirectory()
        if self.repo_path and os.path.isdir(self.repo_path):
            self.repo = git.Repo(self.repo_path)  # Initialize the repo
            self.update_commit_list()  # Display commit history
            # Enable buttons for Git operations
            self.stage_button.config(state=tk.NORMAL)
            self.commit_button.config(state=tk.NORMAL)
            self.push_button.config(state=tk.NORMAL)
            self.pull_button.config(state=tk.NORMAL)
        else:
            # Show error if invalid directory selected
            messagebox.showerror("Error", "Please select a valid Git repository.")

    # Method to update the commit listbox with commit history
    def update_commit_list(self):
        self.commit_listbox.delete(0, tk.END)  # Clear any existing commits
        # Iterate over commits and add them to the listbox
        for commit in self.repo.iter_commits():
            self.commit_listbox.insert(tk.END, f"{commit.hexsha[:7]} - {commit.message.strip()}")

    # Method to stage changes in the repository
    def stage_changes(self):
        try:
            self.repo.git.add(A=True)  # Stage all changes
            messagebox.showinfo("Success", "All changes staged.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stage changes: {str(e)}")

    # Method to commit changes to the repository with a user-provided message
    def commit_changes(self):
        # Prompt user for commit message
        commit_message = simpledialog.askstring("Commit Changes", "Enter commit message:")
        if not commit_message:
            messagebox.showerror("Error", "Commit message cannot be empty.")
            return
        try:
            self.repo.index.commit(commit_message)  # Commit the changes
            messagebox.showinfo("Success", "Changes committed.")
            self.update_commit_list()  # Refresh commit history
        except Exception as e:
            messagebox.showerror("Error", f"Failed to commit changes: {str(e)}")

    # Method to push changes to the remote repository
    def push_changes(self):
        try:
            # Ensure we're using SSH for pushing (check remote URL)
            if "github.com" in self.repo.remotes.origin.url:  # Ensure you're using the SSH URL
                if not self.repo.remotes.origin.url.startswith("git@"):
                    messagebox.showerror("Error", "Repository URL must be an SSH URL for push operation.")
                    return

            # Push changes to remote repository using SSH
            self.repo.git.push()  # This will use SSH if the repository URL is SSH-based
            messagebox.showinfo("Success", "Changes pushed to remote repository.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to push changes: {str(e)}")

    # Method to pull changes from the remote repository
    def pull_changes(self):
        try:
            self.repo.git.pull()  # Pull latest changes from remote
            messagebox.showinfo("Success", "Changes pulled from remote repository.")
            self.update_commit_list()  # Refresh commit history
        except Exception as e:
            messagebox.showerror("Error", f"Failed to pull changes: {str(e)}")

    # Method to clone a new repository based on selected protocol
    def clone_repo(self):
        # Prompt for the Git URL based on SSH/HTTPS selection
        if self.clone_type.get() == "SSH":
            repo_url = simpledialog.askstring("Clone Repository", "Enter the Git SSH URL of the repository (e.g., git@github.com:user/repository.git):")
        else:
            repo_url = simpledialog.askstring("Clone Repository", "Enter the Git HTTPS URL of the repository:")

        if repo_url:
            # Open directory dialog to choose where to clone the repo
            target_dir = filedialog.askdirectory(title="Select Target Directory")
            if target_dir:
                try:
                    # Clone the repository to the selected directory
                    git.Repo.clone_from(repo_url, os.path.join(target_dir, os.path.basename(repo_url)))
                    messagebox.showinfo("Success", f"Repository cloned to {target_dir}.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to clone repository: {str(e)}")
            else:
                messagebox.showerror("Error", "Please select a valid target directory.")
        else:
            messagebox.showerror("Error", "Please enter a valid Git URL.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()  # Initialize the main Tkinter window
    app = GitGUI(root)  # Create an instance of the GitGUI application
    root.mainloop()  # Start the main event loop
