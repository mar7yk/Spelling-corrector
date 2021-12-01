# noinspection PyTypeChecker,PyUnresolvedReferences
def editOperations(s1, s2):

    d = [[None for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]

    d[-1][-1] = [0, None]

    for i in range(len(s1)):
        d[i][-1] = (i + 1, ((i - 1, -1), (s1[i], '')))

    for i in range(len(s2)):
        d[-1][i] = (i + 1, ((-1, i - 1), ('', s2[i])))

    max_dist = max(len(s1), len(s2))

    for i in range(len(s1)):
        for j in range(len(s2)):
            tLen = max_dist
            cost = 1

            if s1[i] == s2[j]:
                cost = 0
            elif i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                tLen = d[i - 2][j - 2][0]

            insertionKey = d[i][j - 1][0] + 1
            deletionKey = d[i - 1][j][0] + 1
            substitutionKey = d[i - 1][j - 1][0] + cost
            transpositionKey = tLen + 1

            options = {
                insertionKey: ((i, j - 1), ('', s2[j])),
                deletionKey: ((i - 1, j), (s1[i], '')),
                substitutionKey: ((i - 1, j - 1), (s1[i], s2[j])),
                transpositionKey: ((i - 2, j - 2), (s1[i - 1] + s1[i], s2[j - 1] + s2[j])),
            }

            key = min(
                insertionKey,
                deletionKey,
                substitutionKey,
                transpositionKey,
            )

            d[i][j] = (key, options[key])

    result = []

    curr = d[len(s1) - 1][len(s2) - 1][1]

    while curr is not None:
        result.insert(0, curr[1])
        curr = d[curr[0][0]][curr[0][1]][1]

    return result
