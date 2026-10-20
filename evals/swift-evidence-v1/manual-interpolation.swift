import SwiftUI
struct BoundedShape: Shape {
 var inset: CGFloat
 var animatableData: CGFloat { get { inset } set { inset = min(max(newValue, 0), 20) } }
 func path(in rect: CGRect) -> Path { Path(rect.insetBy(dx: inset, dy: inset)) }
}
