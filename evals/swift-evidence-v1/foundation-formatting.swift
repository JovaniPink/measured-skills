import Foundation
func labels(_ names: [String], _ number: Double) -> [String] {
 [names.formatted(.list(type: .and)), number.formatted(.number.precision(.fractionLength(2))),
  Date.now.formatted(.dateTime.year().month().day()), URL.documentsDirectory.appending(path: "fixture").lastPathComponent]
}
