import sys
sys.path.insert(0, '.')

from core.matcher import PoetryMatcher

def main():
    print("=" * 60)
    print("Building FAISS Index")
    print("=" * 60)
    
    print("\nInitializing matcher...")
    matcher = PoetryMatcher()
    
    print(f"\nLoaded {matcher.get_quotes_count()} quotes")
    
    if matcher.get_quotes_count() == 0:
        print("ERROR: No quotes found. Run collect_data.py first!")
        return
    
    print("\nBuilding index (this may take a few minutes)...")
    matcher.build_index()
    
    print("\n" + "=" * 60)
    print("Index built successfully!")
    print(f"Index file: data/index.faiss")
    print("=" * 60)

if __name__ == "__main__":
    main()
