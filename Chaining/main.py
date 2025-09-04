from sequence_chain import sequence_chain
from parallel_chain import parallel_chain

# Switch between sequence or parallel
USE_PARALLEL = False

reviews = [
    "I love this smartphone! The camera quality is exceptional and the battery lasts all day. The only downside is that it heats up a bit during gaming.",
    "This laptop is terrible. It's slow, crashes frequently, and the keyboard stopped working after just two months. Customer service was unhelpful.",
]

chain = parallel_chain if USE_PARALLEL else sequence_chain

for review in reviews:
    result = chain.invoke({"review": review})
    print(result)
    print("-" * 40)
