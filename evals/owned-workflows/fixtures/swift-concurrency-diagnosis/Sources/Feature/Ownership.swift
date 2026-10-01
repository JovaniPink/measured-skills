final class MutableBox { var count = 0 }
actor Worker { func receive(_ box: MutableBox) { box.count += 1 } }
@MainActor func send(_ box: MutableBox, to worker: Worker) async {
    await worker.receive(box)
    box.count += 1
}
