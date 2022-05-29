export function computeSum(list) {
  return list.reduce((partialSum, a) => partialSum + a, 0);
}

export function computeAverage(list) {
    return computeSum(list) / list.length
}

export function computeMedian(list) {
    const sorted = Array.from(list).sort((a, b) => a - b);
    const middle = Math.floor(sorted.length / 2);
    if (sorted.length % 2 === 0) {
        return (sorted[middle - 1] + sorted[middle]) / 2;
    }
    return sorted[middle];
}

export function computePercentage(total, subset) {
    if (total == 0) { return 0 }
    return Math.round(subset / total * 100)
}

