import Testing
@testable import ConcurrencyFixture

@Test func withdrawalsCannotOverdrawActorState() async {
    let balance = Balance(10)
    async let first = balance.withdraw(7)
    async let second = balance.withdraw(7)
    let results = await (first, second)
    #expect(results.0 != results.1)
    #expect(await balance.amount == 3)
}

@Test func invalidWithdrawalPreservesState() async {
    let balance = Balance(10)
    #expect(await balance.withdraw(-1) == false)
    #expect(await balance.amount == 10)
}
