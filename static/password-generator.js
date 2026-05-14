class PasswordGenerator {
    constructor() {
        this.UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        this.LOWERCASE = 'abcdefghijklmnopqrstuvwxyz';
        this.DIGITS = '0123456789';
        this.SPECIAL = '!@#$%^&*()-_=+[]{}|;:,.<>?';
        this.CONFUSING = 'O0lI1';

        this.charsets = {
            uppercase: this.UPPERCASE,
            lowercase: this.LOWERCASE,
            digits: this.DIGITS,
            special: this.SPECIAL
        };

        this.policies = {
            standard: { uppercase: 1, lowercase: 1, digits: 1, special: 1, minLength: 8 },
            letters: { uppercase: 1, lowercase: 1, digits: 0, special: 0, minLength: 8 },
            pin: { uppercase: 0, lowercase: 0, digits: 1, special: 0, minLength: 4 },
            custom: null
        };
    }

    secureRandom(max) {
        const array = new Uint32Array(1);
        crypto.getRandomValues(array);
        return array[0] % max;
    }

    generate(length, options = {}) {
        const {
            uppercase = true,
            lowercase = true,
            digits = true,
            special = true,
            excludeConfusing = false
        } = options;

        let charset = '';
        const required = [];

        if (uppercase) {
            let chars = this.UPPERCASE;
            if (excludeConfusing) chars = chars.replace(/[OI]/g, '');
            charset += chars;
            required.push(chars);
        }
        if (lowercase) {
            let chars = this.LOWERCASE;
            if (excludeConfusing) chars = chars.replace(/[l]/g, '');
            charset += chars;
            required.push(chars);
        }
        if (digits) {
            let chars = this.DIGITS;
            if (excludeConfusing) chars = chars.replace(/[01]/g, '');
            charset += chars;
            required.push(chars);
        }
        if (special) {
            charset += this.SPECIAL;
            required.push(this.SPECIAL);
        }

        if (charset.length === 0) {
            throw new Error('至少需要选择一种字符类型');
        }

        const password = [];

        for (const chars of required) {
            if (chars.length > 0) {
                password.push(chars[this.secureRandom(chars.length)]);
            }
        }

        for (let i = password.length; i < length; i++) {
            password.push(charset[this.secureRandom(charset.length)]);
        }

        for (let i = password.length - 1; i > 0; i--) {
            const j = this.secureRandom(i + 1);
            [password[i], password[j]] = [password[j], password[i]];
        }

        return password.join('');
    }

    generateJWTKey(algorithm = 'HS256') {
        const byteLength = algorithm === 'HS512' ? 64 : 32;
        const bytes = new Uint8Array(byteLength);
        crypto.getRandomValues(bytes);

        let binary = '';
        for (let i = 0; i < bytes.length; i++) {
            binary += String.fromCharCode(bytes[i]);
        }

        return btoa(binary)
            .replace(/\+/g, '-')
            .replace(/\//g, '_')
            .replace(/=+$/, '');
    }

    generatePassphrase(wordCount = 4, options = {}) {
        const {
            separator = '-',
            capitalize = false,
            wordlist = typeof WORDLIST !== 'undefined' ? WORDLIST : []
        } = options;

        if (wordlist.length === 0) {
            throw new Error('词表未加载');
        }
        if (wordCount < 4 || wordCount > 10) {
            throw new Error('单词数量必须在 4-10 之间');
        }

        const words = [];
        for (let i = 0; i < wordCount; i++) {
            let word = wordlist[this.secureRandom(wordlist.length)];
            if (capitalize) {
                word = word.charAt(0).toUpperCase() + word.slice(1);
            }
            words.push(word);
        }

        return words.join(separator);
    }

    passphraseEntropy(wordCount, wordlistSize = 2048) {
        return wordCount * Math.log2(wordlistSize);
    }

    generateWithPolicy(length, policyName = 'standard', options = {}) {
        const policy = this.policies[policyName];
        if (!policy) {
            throw new Error('未知策略');
        }

        const maxAttempts = 100;
        for (let attempt = 0; attempt < maxAttempts; attempt++) {
            const password = this.generate(length, options);
            if (this.validatePolicy(password, policy)) {
                return password;
            }
        }

        throw new Error('无法生成满足策略的密码，请增加长度或放宽条件');
    }

    validatePolicy(password, policy) {
        const counts = {
            uppercase: 0,
            lowercase: 0,
            digits: 0,
            special: 0
        };

        for (const char of password) {
            if (this.UPPERCASE.includes(char)) counts.uppercase++;
            else if (this.LOWERCASE.includes(char)) counts.lowercase++;
            else if (this.DIGITS.includes(char)) counts.digits++;
            else if (this.SPECIAL.includes(char)) counts.special++;
        }

        return (
            counts.uppercase >= (policy.uppercase || 0) &&
            counts.lowercase >= (policy.lowercase || 0) &&
            counts.digits >= (policy.digits || 0) &&
            counts.special >= (policy.special || 0)
        );
    }

    keyToHex(base64url) {
        const base64 = base64url.replace(/-/g, '+').replace(/_/g, '/');
        const binary = atob(base64);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) {
            bytes[i] = binary.charCodeAt(i);
        }
        return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
    }

    keyToEnv(base64url) {
        return `JWT_SECRET=${base64url}`;
    }

    getKeyFormats(base64url, algorithm = 'HS256') {
        return {
            base64url,
            hex: this.keyToHex(base64url),
            env: this.keyToEnv(base64url)
        };
    }

    calcEntropy(password, charsetSize) {
        if (charsetSize === 0) return 0;
        return password.length * Math.log2(charsetSize);
    }

    getCharsetSize(options = {}) {
        const {
            uppercase = true,
            lowercase = true,
            digits = true,
            special = true,
            excludeConfusing = false
        } = options;

        let size = 0;
        if (uppercase) size += excludeConfusing ? 24 : 26;
        if (lowercase) size += excludeConfusing ? 25 : 26;
        if (digits) size += excludeConfusing ? 8 : 10;
        if (special) size += this.SPECIAL.length;
        return size;
    }

    strengthLabel(entropy) {
        if (entropy < 50) return { label: '弱', color: '#e74c3c' };
        if (entropy < 80) return { label: '中等', color: '#f39c12' };
        if (entropy < 120) return { label: '强', color: '#27ae60' };
        return { label: '非常强', color: '#00bcd4' };
    }

    getPasswordInfo(password, options = {}) {
        const charsetSize = this.getCharsetSize(options);
        const entropy = this.calcEntropy(password, charsetSize);
        const strength = this.strengthLabel(entropy);

        return {
            password,
            length: password.length,
            entropy: Math.round(entropy * 10) / 10,
            strength: strength.label,
            strengthColor: strength.color
        };
    }
}

const passwordGenerator = new PasswordGenerator();
