#!/usr/bin/env python3
"""
🔐 Password Generator CLI
Generate secure passwords with customizable options.
"""

import argparse
import secrets
import string
import sys
from pathlib import Path

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class PasswordGenerator:
    """Generate cryptographically secure passwords."""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous = "0O1lI"
    
    def generate(
        self,
        length: int = 16,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
        exclude_ambiguous: bool = False
    ) -> str:
        """Generate a secure password."""
        
        charset = ""
        required_chars = []
        
        if use_lowercase:
            chars = self.lowercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_uppercase:
            chars = self.uppercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_digits:
            chars = self.digits
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_symbols:
            charset += self.symbols
            required_chars.append(secrets.choice(self.symbols))
        
        if not charset:
            print("Error: At least one character type must be selected!")
            sys.exit(1)
        
        if length < len(required_chars):
            print(f"Error: Length must be at least {len(required_chars)} characters!")
            sys.exit(1)
        
        # Generate remaining characters
        remaining_length = length - len(required_chars)
        password_chars = required_chars + [secrets.choice(charset) for _ in range(remaining_length)]
        
        # Shuffle to avoid predictable positions
        password_list = list(password_chars)
        for i in range(len(password_list) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_list[i], password_list[j] = password_list[j], password_list[i]
        
        return ''.join(password_list)
    
    def analyze_strength(self, password: str) -> dict:
        """Analyze password strength."""
        
        strength = {
            'length': len(password),
            'has_uppercase': any(c.isupper() for c in password),
            'has_lowercase': any(c.islower() for c in password),
            'has_digits': any(c.isdigit() for c in password),
            'has_symbols': any(c in self.symbols for c in password),
        }
        
        # Calculate score
        score = 0
        if strength['length'] >= 8:
            score += 1
        if strength['length'] >= 12:
            score += 1
        if strength['length'] >= 16:
            score += 1
        if strength['has_uppercase']:
            score += 1
        if strength['has_lowercase']:
            score += 1
        if strength['has_digits']:
            score += 1
        if strength['has_symbols']:
            score += 1
        
        if score <= 2:
            strength['level'] = 'WEAK'
        elif score <= 4:
            strength['level'] = 'MEDIUM'
        elif score <= 5:
            strength['level'] = 'STRONG'
        else:
            strength['level'] = 'VERY STRONG'
        
        return strength
    
    def print_strength(self, password: str):
        """Print password strength analysis."""
        
        strength = self.analyze_strength(password)
        
        print(f"\nPassword: {password}")
        print(f"\n📊 Password Strength: {strength['level']}")
        print(f"├── Length: {strength['length']} characters {'✓' if strength['length'] >= 8 else '✗'}")
        print(f"├── Uppercase: {'Yes ✓' if strength['has_uppercase'] else 'No ✗'}")
        print(f"├── Lowercase: {'Yes ✓' if strength['has_lowercase'] else 'No ✗'}")
        print(f"├── Numbers: {'Yes ✓' if strength['has_digits'] else 'No ✗'}")
        print(f"└── Symbols: {'Yes ✓' if strength['has_symbols'] else 'No ✗'}")


def main():
    parser = argparse.ArgumentParser(
        description="🔐 Secure Password Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    Generate a 16-character password
  %(prog)s -l 32             Generate a 32-character password
  %(prog)s -u -d -s          Only uppercase, digits, and symbols
  %(prog)s -n 5              Generate 5 passwords
  %(prog)s -c                Copy to clipboard
  %(prog)s --analyze "MyP@ss"  Analyze password strength
        """
    )
    
    parser.add_argument('-l', '--length', type=int, default=16,
                       help='Password length (default: 16)')
    parser.add_argument('-n', '--count', type=int, default=1,
                       help='Number of passwords to generate')
    parser.add_argument('-u', '--uppercase', action='store_true', default=True,
                       help='Include uppercase letters')
    parser.add_argument('-U', '--no-uppercase', action='store_true',
                       help='Exclude uppercase letters')
    parser.add_argument('-d', '--digits', action='store_true', default=True,
                       help='Include digits')
    parser.add_argument('-D', '--no-digits', action='store_true',
                       help='Exclude digits')
    parser.add_argument('-s', '--symbols', action='store_true', default=True,
                       help='Include symbols')
    parser.add_argument('-S', '--no-symbols', action='store_true',
                       help='Exclude symbols')
    parser.add_argument('--no-ambiguous', action='store_true',
                       help='Exclude ambiguous characters (0, O, l, 1, I)')
    parser.add_argument('-c', '--clipboard', action='store_true',
                       help='Copy to clipboard')
    parser.add_argument('-o', '--output', type=str,
                       help='Save to file')
    parser.add_argument('--analyze', type=str, metavar='PASSWORD',
                       help='Analyze password strength')
    
    args = parser.parse_args()
    
    generator = PasswordGenerator()
    
    # Analyze mode
    if args.analyze:
        generator.print_strength(args.analyze)
        return
    
    # Generate passwords
    for i in range(args.count):
        password = generator.generate(
            length=args.length,
            use_uppercase=not args.no_uppercase,
            use_lowercase=True,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_ambiguous=args.no_ambiguous
        )
        
        print(password)
        
        # Copy to clipboard
        if args.clipboard and CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)
            print("✓ Copied to clipboard!")
    
    # Save to file
    if args.output:
        passwords = [
            generator.generate(
                length=args.length,
                use_uppercase=not args.no_uppercase,
                use_lowercase=True,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
                exclude_ambiguous=args.no_ambiguous
            )
            for _ in range(args.count)
        ]
        
        with open(args.output, 'w') as f:
            f.write('\n'.join(passwords))
        
        print(f"\n✓ Saved {args.count} passwords to {args.output}")


if __name__ == "__main__":
    main()
