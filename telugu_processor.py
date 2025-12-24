"""
Module for detecting and processing Telugu Unicode text.
"""
import re
from typing import List, Dict, Tuple
import unicodedata


def detect_telugu_unicode(text: str) -> Dict:
    """
    Detect Telugu characters in Unicode text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with detection results
    """
    # Telugu Unicode range: U+0C00 to U+0C7F
    telugu_pattern = r'[\u0C00-\u0C7F]'
    telugu_matches = re.findall(telugu_pattern, text)
    
    # Find all Telugu characters with their positions
    telugu_chars_with_pos = []
    for match in re.finditer(telugu_pattern, text):
        telugu_chars_with_pos.append({
            'char': match.group(),
            'start_pos': match.start(),
            'end_pos': match.end(),
            'unicode_code': f'U+{ord(match.group()):04X}'
        })
    
    # Count unique Telugu characters
    unique_telugu_chars = list(set(telugu_matches))
    
    # Calculate statistics
    total_chars = len(text)
    telugu_char_count = len(telugu_matches)
    telugu_unique_count = len(unique_telugu_chars)
    telugu_percentage = (telugu_char_count / total_chars * 100) if total_chars > 0 else 0
    
    return {
        'has_telugu': len(telugu_matches) > 0,
        'total_telugu_chars': telugu_char_count,
        'unique_telugu_chars': telugu_unique_count,
        'telugu_percentage': telugu_percentage,
        'telugu_chars': telugu_matches,
        'unique_chars_list': unique_telugu_chars,
        'telugu_chars_with_positions': telugu_chars_with_pos,
        'first_telugu_pos': telugu_chars_with_pos[0]['start_pos'] if telugu_chars_with_pos else -1,
        'last_telugu_pos': telugu_chars_with_pos[-1]['start_pos'] if telugu_chars_with_pos else -1
    }


def normalize_telugu_text(text: str) -> str:
    """
    Normalize Telugu text by handling common Unicode issues.
    
    Args:
        text: Input text containing Telugu characters
        
    Returns:
        Normalized text
    """
    # Normalize Unicode combining characters
    normalized_text = unicodedata.normalize('NFC', text)
    
    # Remove any invisible or problematic control characters
    # but preserve legitimate Telugu characters
    cleaned_text = ''.join(
        char for char in normalized_text 
        if unicodedata.category(char)[0] != 'C' or char in '\t\n\r' or not ('\u0C00' <= char <= '\u0C7F')
    )
    
    return cleaned_text


def convert_telugu_unicode_to_readable(text: str) -> Dict:
    """
    Process Telugu Unicode text to make it properly readable.

    Args:
        text: Input text with Telugu Unicode

    Returns:
        Dictionary with original, processed text and processing info
    """
    original_text = text

    # Detect Telugu in the text
    detection_result = detect_telugu_unicode(text)

    if not detection_result['has_telugu']:
        return {
            'original_text': original_text,
            'processed_text': text,
            'is_telugu_present': False,
            'processing_applied': False,
            'detection_info': detection_result
        }

    # Normalize the text
    normalized_text = normalize_telugu_text(text)

    # Additional processing specific to Telugu if needed
    # For now, we'll just return the normalized text
    processed_text = normalized_text

    return {
        'original_text': original_text,
        'processed_text': processed_text,
        'is_telugu_present': True,
        'processing_applied': True,
        'detection_info': detection_result,
        'normalization_applied': True
    }


def extract_telugu_sentences(text: str) -> List[str]:
    """
    Extract sentences that contain Telugu text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        List of sentences containing Telugu text
    """
    # Split text into sentences using common delimiters
    sentences = re.split(r'[.!?।॥\n]+', text)
    
    telugu_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and detect_telugu_unicode(sentence)['has_telugu']:
            telugu_sentences.append(sentence)
    
    return telugu_sentences


def get_telugu_word_stats(text: str) -> Dict:
    """
    Get statistics about Telugu words in the text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with Telugu word statistics
    """
    # Find sequences of Telugu characters (potential words)
    telugu_word_pattern = r'[\u0C00-\u0C7F]+'
    telugu_words = re.findall(telugu_word_pattern, text)
    
    # Calculate word statistics
    word_lengths = [len(word) for word in telugu_words]
    avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
    
    # Count unique words
    unique_words = list(set(telugu_words))
    
    return {
        'total_telugu_words': len(telugu_words),
        'unique_telugu_words': len(unique_words),
        'avg_word_length': avg_word_length,
        'telugu_words': telugu_words,
        'unique_words': unique_words,
        'word_length_distribution': {
            'min': min(word_lengths) if word_lengths else 0,
            'max': max(word_lengths) if word_lengths else 0,
            'avg': avg_word_length
        }
    }


def validate_telugu_unicode(text: str) -> Dict:
    """
    Validate Telugu Unicode in the text and check for any issues.
    
    Args:
        text: Input text to validate
        
    Returns:
        Dictionary with validation results
    """
    detection_result = detect_telugu_unicode(text)
    
    issues = []
    
    # Check for invalid Telugu Unicode sequences
    for match in re.finditer(r'[\u0C00-\u0C7F]', text):
        char = match.group()
        # Check if character is a valid Telugu character
        # In Telugu script, consonants and vowels have specific patterns
        # This is a simplified validation
        code_point = ord(char)
        
        # Check if the character is in the valid Telugu range but might be a control character
        if 0x0C00 <= code_point <= 0x0C03:  # Telugu signs
            continue  # These are valid
        elif 0x0C12 <= code_point <= 0x0C28:  # Basic Telugu letters
            continue  # These are valid
        elif 0x0C2A <= code_point <= 0x0C39:  # More Telugu letters
            continue  # These are valid
        elif 0x0C3E <= code_point <= 0x0C4C:  # Vowel signs
            continue  # These are valid
        elif 0x0C55 <= code_point <= 0x0C56:  # Length marks
            continue  # These are valid
        elif 0x0C60 <= code_point <= 0x0C61:  # Vocalics
            continue  # These are valid
        elif 0x0C62 <= code_point <= 0x0C63:  # More vocalics
            continue  # These are valid
        elif 0x0C78 <= code_point <= 0x0C7F:  # Telugu fraction digits
            continue  # These are valid
        else:
            issues.append({
                'char': char,
                'code_point': f'U+{code_point:04X}',
                'position': match.start(),
                'issue': 'Potentially invalid Telugu character'
            })
    
    return {
        'is_valid': len(issues) == 0,
        'detection_info': detection_result,
        'validation_issues': issues,
        'validation_passed': len(issues) == 0
    }


