# 🔐 Password Generator CLI

A secure command-line password generator built with Python.

## ✨ Features
- Generate passwords of any length
- Include/exclude uppercase, lowercase, numbers, symbols
- Copy to clipboard support
- Password strength analysis
- Save passwords to file (encrypted)
- Batch generation support

## 🛠️ Tech Stack
- **Language:** Python 3.8+
- **Libraries:** `secrets`, `string`, `argparse`, `pyperclip`

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/password-generator.git

# Navigate to directory
cd password-generator

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Usage
```bash
# Generate a 16-character password
python password_generator.py

# Generate a 32-character password
python password_generator.py -l 32

# Generate with only uppercase and numbers
python password_generator.py -u -d -s
```

### Advanced Options
```bash
# Generate 5 passwords at once
python password_generator.py -n 5

# Copy to clipboard
python password_generator.py -c

# Save to file
python password_generator.py -o passwords.txt

# Exclude ambiguous characters (0, O, l, 1, I)
python password_generator.py --no-ambiguous
```

## 📊 Password Strength Analysis
```bash
python password_generator.py --analyze "MyP@ssw0rd"
```

Output:
```
Password Strength: STRONG
├── Length: 10 characters ✓
├── Uppercase: Yes ✓
├── Lowercase: Yes ✓
├── Numbers: Yes ✓
└── Symbols: Yes ✓
```

## 🔒 Security Features
- Uses `secrets` module for cryptographically secure random numbers
- Never stores passwords in plain text
- Supports AES encryption for saved files
- No network requests - works offline

## 📁 Project Structure
```
password-generator/
├── password_generator.py    # Main script
├── strength_analyzer.py     # Password strength checker
├── encryptor.py            # File encryption utilities
├── requirements.txt        # Dependencies
└── README.md
```

## 🤝 Contributing
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---

Made with ❤️ by [Your Name]
