from __future__ import annotations

from profile_store import ProfileStore


def main() -> None:
    store = ProfileStore()
    print("Setup your profile for form filling. Press Enter to keep current values.\n")
    profile = store.load()
    questions = {
        "name": "Full name",
        "email": "Email",
        "phone": "Phone",
        "college": "College / university",
        "linkedin": "LinkedIn URL",
        "portfolio": "Portfolio URL",
        "github": "GitHub URL",
        "address": "Address",
        "bio": "Short bio",
        "sop": "Short SOP",
    }
    for key, label in questions.items():
        current = profile.get(key, "")
        value = input(f"{label} [{current}]: ").strip()
        if value:
            profile[key] = value

    resume_path = input("Resume file path (optional): ").strip()
    if resume_path:
        profile["resume_path"] = resume_path

    store.save(profile)
    print("\nProfile saved to:", store.path)


if __name__ == "__main__":
    main()
