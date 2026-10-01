actor Ledger {
    var balance = 10
    func spend(_ amount: Int, approval: () async -> Bool) async {
        guard balance >= amount else { return }
        guard await approval() else { return }
        balance -= amount
    }
}
