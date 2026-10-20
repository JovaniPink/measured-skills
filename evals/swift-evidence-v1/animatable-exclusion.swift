import SwiftUI
@Animatable struct InsetShape: Shape {
 var inset: CGFloat
 @AnimatableIgnored var enabled: Bool
 func path(in rect: CGRect) -> Path { Path(rect.insetBy(dx: inset, dy: inset)) }
}
