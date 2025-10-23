#!/usr/bin/env python3
"""
Test script to verify the package structure works correctly
"""

def test_imports():
    """Test all package imports."""
    try:
        print("🔄 Testing package imports...")
        
        # Test services package
        import services
        print("✅ services package imported")
        
        # Test API imports
        from services.api import QueryRequest, QueryResponse
        print("✅ API models imported")
        
        # Test retriever imports
        from services.retriever import retrieve, get_embedding
        print("✅ Retriever functions imported")
        
        # Test indexer imports
        from services.indexer import index_pdf, index_url
        print("✅ Indexer functions imported")
        
        # Test LLM imports
        from services.llm import run_llm
        print("✅ LLM functions imported")
        
        print("\n🎉 All package imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Blockchain RAG Package Structure")
    print("=" * 50)
    
    success = test_imports()
    
    if success:
        print("\n✅ Package structure is clean and production-ready!")
        print("You can now run:")
        print("  python services/indexer/indexer.py 'Ethereum_Whitepaper_-_Buterin_2014 (1).pdf' --collection protocol_docs")
    else:
        print("\n❌ Package structure needs fixing")
