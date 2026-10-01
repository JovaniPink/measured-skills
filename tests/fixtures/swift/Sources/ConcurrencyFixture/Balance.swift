public actor Balance {
    public private(set) var amount: Int
    public init(_ amount: Int) { self.amount = amount }
    public func withdraw(_ value: Int) -> Bool {
        guard value >= 0, amount >= value else { return false }
        amount -= value
        return true
    }
}
