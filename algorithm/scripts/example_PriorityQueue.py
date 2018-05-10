import heapq

pq = []
heapq.heappush(pq, (2, "due"))
heapq.heappush(pq, (10, "dieci"))
heapq.heappush(pq, (1, "uno"))
heapq.heappush(pq, (5, "cinque"))
heapq.heappush(pq, (9, "nove"))
heapq.heappush(pq, (0, "zero"))
heapq.heappush(pq, (-5, "menocinque"))

while not len(pq) == 0:
    print (heapq.heappop(pq)[1])