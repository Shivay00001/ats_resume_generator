
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.scrolledtext as scrolledtext
import os

from constants import ROLE_KEYWORDS, ACTION_VERBS
import ats_logic
import generator

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas = canvas

class ATSResumeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATS-Friendly Resume Generator (100% Parsable)")
        self.geometry("1400x900")
        
        # Data containers
        self.experience_frames = []
        self.project_frames = []
        self.education_frames = []

        # Paned Window
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left Pane: Input Form
        self.left_frame = ttk.Frame(self.paned_window, width=700)
        self.paned_window.add(self.left_frame, weight=1)
        
        self.form_container = ScrollableFrame(self.left_frame)
        self.form_container.pack(fill=tk.BOTH, expand=True)
        self.form_frame = self.form_container.scrollable_frame
        
        # Right Pane: Preview & helper
        self.right_frame = ttk.Frame(self.paned_window, width=500)
        self.paned_window.add(self.right_frame, weight=1)

        self._build_form()
        self._build_sidebar()
        
        # Mousewheel scroll support
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.form_container.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _build_form(self):
        # 1. Target Role & Keywords
        self._add_section_header("Step 0: Target Role (For Optimization)", 0)
        
        target_frame = ttk.Frame(self.form_frame)
        target_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        ttk.Label(target_frame, text="Target Role:").pack(side=tk.LEFT)
        self.role_var = tk.StringVar()
        self.role_combo = ttk.Combobox(target_frame, textvariable=self.role_var, values=list(ROLE_KEYWORDS.keys()))
        self.role_combo.pack(side=tk.LEFT, padx=5)
        self.role_combo.bind("<<ComboboxSelected>>", self._update_suggestions)
        
        ttk.Button(target_frame, text="Inject Keywords to Skills", command=self._inject_keywords).pack(side=tk.LEFT, padx=10)

        # 2. Contact Info
        self._add_section_header("Step 1: Contact Information", 2)
        contact_frame = ttk.Frame(self.form_frame)
        contact_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        
        self.entries = {}
        fields = [("Full Name", "full_name"), ("Email", "email"), ("Phone", "phone"), 
                  ("City", "city"), ("Country", "country"), ("LinkedIn URL", "linkedin"), 
                  ("GitHub/Portfolio", "github")]
        
        for i, (label, key) in enumerate(fields):
            r = i // 2
            c = (i % 2) * 2
            ttk.Label(contact_frame, text=label).grid(row=r, column=c, sticky="w", padx=5, pady=2)
            ent = ttk.Entry(contact_frame, width=30)
            ent.grid(row=r, column=c+1, sticky="w", padx=5, pady=2)
            self.entries[key] = ent
            
        # 3. Professional Summary
        self._add_section_header("Step 2: Professional Summary", 4)
        self.summary_text = scrolledtext.ScrolledText(self.form_frame, height=5, width=80)
        self.summary_text.grid(row=5, column=0, padx=10, pady=5)
        
        # 4. Skills
        self._add_section_header("Step 3: Skills (Comma Separated)", 6)
        self.skills_text = scrolledtext.ScrolledText(self.form_frame, height=3, width=80)
        self.skills_text.grid(row=7, column=0, padx=10, pady=5)
        
        # 5. Work Experience (Dynamic)
        self._add_section_header("Step 4: Work Experience", 8)
        self.exp_container = ttk.Frame(self.form_frame)
        self.exp_container.grid(row=9, column=0, sticky="ew", padx=10)
        ttk.Button(self.form_frame, text="+ Add Job", command=self._add_experience).grid(row=10, column=0, pady=5)
        self._add_experience() # Add one default

        # 6. Projects (Dynamic)
        self._add_section_header("Step 5: Projects", 11)
        self.proj_container = ttk.Frame(self.form_frame)
        self.proj_container.grid(row=12, column=0, sticky="ew", padx=10)
        ttk.Button(self.form_frame, text="+ Add Project", command=self._add_project).grid(row=13, column=0, pady=5)
        # self._add_project() 
        
        # 7. Education (Dynamic)
        self._add_section_header("Step 6: Education", 14)
        self.edu_container = ttk.Frame(self.form_frame)
        self.edu_container.grid(row=15, column=0, sticky="ew", padx=10)
        ttk.Button(self.form_frame, text="+ Add Education", command=self._add_education).grid(row=16, column=0, pady=5)
        self._add_education()

        # 8. Certifications
        self._add_section_header("Step 7: Certifications (One per line)", 17)
        self.cert_text = scrolledtext.ScrolledText(self.form_frame, height=4, width=80)
        self.cert_text.grid(row=18, column=0, padx=10, pady=5, list=20) # list=20 is padding bottom

    def _add_section_header(self, text, row):
        lbl = ttk.Label(self.form_frame, text=text, font=("Arial", 11, "bold"), background="#ddd")
        lbl.grid(row=row, column=0, sticky="ew", padx=5, pady=(15, 5))

    def _add_experience(self):
        # A frame for one job
        frame = ttk.LabelFrame(self.exp_container, text=f"Job {len(self.experience_frames)+1}")
        frame.pack(fill="x", pady=5)
        
        entries = {}
        # Line 1: Company, Location
        f1 = ttk.Frame(frame)
        f1.pack(fill="x")
        ttk.Label(f1, text="Company:").pack(side=tk.LEFT)
        e_comp = ttk.Entry(f1, width=25)
        e_comp.pack(side=tk.LEFT, padx=5)
        entries['company'] = e_comp
        
        ttk.Label(f1, text="Location:").pack(side=tk.LEFT)
        e_loc = ttk.Entry(f1, width=20)
        e_loc.pack(side=tk.LEFT, padx=5)
        entries['location'] = e_loc
        
        # Line 2: Title, Dates (Start - End)
        f2 = ttk.Frame(frame)
        f2.pack(fill="x", pady=2)
        ttk.Label(f2, text="Title:").pack(side=tk.LEFT)
        e_title = ttk.Entry(f2, width=25)
        e_title.pack(side=tk.LEFT, padx=5)
        entries['title'] = e_title
        
        ttk.Label(f2, text="Start:").pack(side=tk.LEFT)
        e_start = ttk.Entry(f2, width=10)
        e_start.pack(side=tk.LEFT, padx=2)
        entries['start_date'] = e_start

        ttk.Label(f2, text="End:").pack(side=tk.LEFT)
        e_end = ttk.Entry(f2, width=10)
        e_end.pack(side=tk.LEFT, padx=2)
        entries['end_date'] = e_end
        
        # Line 3: Description (Bullets)
        ttk.Label(frame, text="Responsibilities (Bullets):").pack(anchor="w")
        t_resp = scrolledtext.ScrolledText(frame, height=4, width=70)
        t_resp.pack(fill="x", padx=5, pady=2)
        entries['responsibilities'] = t_resp
        
        # Delete Button
        btn_del = ttk.Button(frame, text="Remove Job", command=lambda f=frame: self._remove_frame(f, self.experience_frames))
        btn_del.pack(anchor="e")

        self.experience_frames.append((frame, entries))

    def _add_project(self):
        frame = ttk.LabelFrame(self.proj_container, text=f"Project {len(self.project_frames)+1}")
        frame.pack(fill="x", pady=5)
        
        entries = {}
        f1 = ttk.Frame(frame)
        f1.pack(fill="x")
        ttk.Label(f1, text="Project Name:").pack(side=tk.LEFT)
        e_name = ttk.Entry(f1, width=40)
        e_name.pack(side=tk.LEFT, padx=5)
        entries['name'] = e_name
        
        ttk.Label(frame, text="Description (Bullets):").pack(anchor="w")
        t_desc = scrolledtext.ScrolledText(frame, height=3, width=70)
        t_desc.pack(fill="x", padx=5, pady=2)
        entries['description'] = t_desc
        
        btn_del = ttk.Button(frame, text="Remove Project", command=lambda f=frame: self._remove_frame(f, self.project_frames))
        btn_del.pack(anchor="e")

        self.project_frames.append((frame, entries))

    def _add_education(self):
        frame = ttk.LabelFrame(self.edu_container, text=f"Education {len(self.education_frames)+1}")
        frame.pack(fill="x", pady=5)
        
        entries = {}
        f1 = ttk.Frame(frame)
        f1.pack(fill="x")
        ttk.Label(f1, text="School:").pack(side=tk.LEFT)
        e_school = ttk.Entry(f1, width=25)
        e_school.pack(side=tk.LEFT, padx=5)
        entries['institution'] = e_school
        
        ttk.Label(f1, text="Degree:").pack(side=tk.LEFT)
        e_deg = ttk.Entry(f1, width=25)
        e_deg.pack(side=tk.LEFT, padx=5)
        entries['degree'] = e_deg
        
        ttk.Label(f1, text="Year:").pack(side=tk.LEFT)
        e_year = ttk.Entry(f1, width=10)
        e_year.pack(side=tk.LEFT, padx=5)
        entries['year'] = e_year
        
        btn_del = ttk.Button(frame, text="Remove", command=lambda f=frame: self._remove_frame(f, self.education_frames))
        btn_del.pack(anchor="e")

        self.education_frames.append((frame, entries))

    def _remove_frame(self, frame, list_ref):
        frame.destroy()
        # Filter out destroyed frames from the list tuple
        # This is a bit tricky since we stored (frame, entries), so we need to find the index
        for i, (f, _) in enumerate(list_ref):
            if f == frame:
                list_ref.pop(i)
                break
    
    def _build_sidebar(self):
        # Stats & Checks
        stats_frame = ttk.LabelFrame(self.right_frame, text="ATS Optimization & Quality Check")
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        self.score_label = ttk.Label(stats_frame, text="ATS Score: - / 100", font=("Arial", 14, "bold"))
        self.score_label.pack(pady=5)
        
        self.feedback_list = tk.Listbox(stats_frame, height=8)
        self.feedback_list.pack(fill="x", padx=5, pady=5)
        
        # Action Buttons
        btn_frame = ttk.Frame(self.right_frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Check Score & Preview", command=self._update_preview).pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Export to DOCX", command=lambda: self._export("docx")).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="Export to PDF (Plain)", command=lambda: self._export("pdf")).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="Export to TXT", command=lambda: self._export("txt")).pack(fill="x", pady=2)

        # Keyword Suggestions
        kw_frame = ttk.LabelFrame(self.right_frame, text="Suggested Keywords for Role")
        kw_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.kw_listbox = tk.Listbox(kw_frame)
        self.kw_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Plain Text Preview
        prev_frame = ttk.LabelFrame(self.right_frame, text="Plain Text Preview")
        prev_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.preview_text = scrolledtext.ScrolledText(prev_frame, height=15)
        self.preview_text.pack(fill="both", expand=True, padx=5, pady=5)

    def _collect_data(self):
        """Scrapes data from all UI fields"""
        data = {key: entry.get() for key, entry in self.entries.items()}
        data['summary'] = self.summary_text.get("1.0", tk.END).strip()
        data['skills'] = self.skills_text.get("1.0", tk.END).strip()
        
        # Experience
        data['experience'] = []
        for _, entries in self.experience_frames:
            job = {k: v.get("1.0", tk.END).strip() if isinstance(v, tk.Text) else v.get() for k, v in entries.items()}
            if job.get('company') or job.get('title'):
                data['experience'].append(job)

        # Projects
        data['projects'] = []
        for _, entries in self.project_frames:
            proj = {k: v.get("1.0", tk.END).strip() if isinstance(v, tk.Text) else v.get() for k, v in entries.items()}
            if proj.get('name'):
                data['projects'].append(proj)

        # Education
        data['education'] = []
        for _, entries in self.education_frames:
            edu = {k: v.get() for k, v in entries.items()}
            if edu.get('institution'):
                data['education'].append(edu)

        # Certifications
        certs = self.cert_text.get("1.0", tk.END).strip().split('\n')
        data['certifications'] = [c for c in certs if c.strip()]

        return data

    def _update_suggestions(self, event=None):
        role = self.role_var.get()
        keywords = ats_logic.get_role_keywords(role)
        self.kw_listbox.delete(0, tk.END)
        for kw in keywords:
            self.kw_listbox.insert(tk.END, kw)

    def _inject_keywords(self):
        role = self.role_var.get()
        if not role:
            messagebox.showwarning("No Role Selected", "Please select a target role first.")
            return
            
        keywords = ats_logic.get_role_keywords(role)
        current_skills = self.skills_text.get("1.0", tk.END).strip()
        
        new_keywords = [k for k in keywords if k.lower() not in current_skills.lower()]
        
        if new_keywords:
            if current_skills:
                self.skills_text.insert(tk.END, ", " + ", ".join(new_keywords))
            else:
                self.skills_text.insert(tk.END, ", ".join(new_keywords))
            messagebox.showinfo("Injected", f"Added {len(new_keywords)} keywords for {role}.")
        else:
            messagebox.showinfo("Info", "Keywords already present.")

    def _update_preview(self):
        data = self._collect_data()
        
        # Score
        score, feedback = ats_logic.calculate_ats_score(data)
        self.score_label.config(text=f"ATS Score: {score} / 100", foreground="green" if score > 80 else "red")
        
        self.feedback_list.delete(0, tk.END)
        for item in feedback:
            self.feedback_list.insert(tk.END, item)
            
        # Preview Text
        # Generate a temp txt file content in memory to show
        # We can reuse the logic in generator but we want string return
        # Let's just create a quick preview string
        preview_str = f"--- START PREVIEW ---\n"
        preview_str += f"NAME: {data.get('full_name')}\n"
        preview_str += f"SUMMARY: {data.get('summary')}\n"
        preview_str += f"SKILLS: {data.get('skills')}\n"
        preview_str += f"\n[EXPERIENCE]:\n"
        for exp in data.get('experience', []):
            preview_str += f"* {exp.get('title')} at {exp.get('company')}\n"
        preview_str += f"--- END PREVIEW ---\n"
        
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, preview_str)

    def _export(self, fmt):
        data = self._collect_data()
        # Basic Validation
        if not data.get('full_name'):
            messagebox.showerror("Error", "Full Name is required.")
            return
            
        file_types = []
        if fmt == 'docx': file_types = [("Word Document", "*.docx")]
        elif fmt == 'pdf': file_types = [("PDF Document", "*.pdf")]
        else: file_types = [("Text File", "*.txt")]

        path = filedialog.asksaveasfilename(defaultextension=f".{fmt}", filetypes=file_types)
        if path:
            try:
                generator.generate_resume(data, path, fmt)
                messagebox.showinfo("Success", f"Saved to {path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")

if __name__ == "__main__":
    try:
        app = ATSResumeApp()
        app.mainloop()
    except Exception as e:
        # Fallback for debugging if something crashes immediately
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
