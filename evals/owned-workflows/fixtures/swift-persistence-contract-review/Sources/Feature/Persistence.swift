import Foundation
struct StoredRecord: Codable { let id: UUID; var title: String; var modifiedAt: Date; var deletedAt: Date? }
final class RecordOwner {
    var rows: [StoredRecord] = []
    func save(_ record: StoredRecord) { rows.append(record) }
}
func saveFromView(_ record: StoredRecord, owner: RecordOwner) { owner.rows.append(record) }
func deleteFromView(_ id: UUID, owner: RecordOwner) { owner.rows.removeAll { $0.id == id } }
