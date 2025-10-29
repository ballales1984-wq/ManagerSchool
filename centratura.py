"""
Modulo per la centratura di versi poetici.
Funzione essenziale per allineare al centro un testo.
"""


def centratura(versi):
    """
    Centra una lista di versi in base al verso più lungo.
    
    Args:
        versi: Lista di stringhe (versi)
        
    Returns:
        Lista di versi centrati
    """
    max_len = max(len(verso) for verso in versi)
    return [(' ' * ((max_len - len(verso)) // 2)) + verso for verso in versi]


if __name__ == "__main__":
    # Test della funzione
    test_versi = [
        "Nel mezzo del cammin",
        "di nostra vita",
        "mi ritrovai",
        "per una selva oscura"
    ]
    
    print("Versi originali:")
    for verso in test_versi:
        print(f"'{verso}'")
    
    print("\nVersi centrati:")
    centrati = centratura(test_versi)
    for verso in centrati:
        print(f"'{verso}'")

