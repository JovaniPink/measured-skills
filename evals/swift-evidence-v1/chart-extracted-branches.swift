import SwiftUI
import Charts
struct Metric: Identifiable { var id: Int; var value: Double }
struct ChartProbe: View {
 let rows: [Metric]; let selected: Int
 var body: some View { Chart(rows) { row in marks(row) } }
 @ChartContentBuilder private func marks(_ row: Metric) -> some ChartContent {
  switch selected {
   case 0: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 0))
   case 1: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 1))
   case 2: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 2))
   case 3: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 3))
   case 4: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 4))
   case 5: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 5))
   case 6: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 6))
   case 7: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 7))
   case 8: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 8))
   case 9: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 9))
   case 10: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 10))
   case 11: LineMark(x: .value("Position", row.id), y: .value("Metric", row.value + 11))
   default: PointMark(x: .value("Position", row.id), y: .value("Metric", row.value))
  }
 }
}
