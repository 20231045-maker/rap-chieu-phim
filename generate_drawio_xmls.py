# Script tạo các file .drawio XML chuẩn để mở trực tiếp trên app.diagrams.net hoặc phần mềm draw.io
import os

drawio_dir = os.path.join('report_assets', 'drawio')
os.makedirs(drawio_dir, exist_ok=True)

# 1. FDD Draw.io XML
fdd_xml = """<mxfile host="app.diagrams.net" modified="2026-10-13T16:00:00.000Z" agent="Antigravity" version="24.0.0">
  <diagram id="FDD_Diagram" name="Biểu đồ phân cấp chức năng FDD">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="root_node" value="HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU RẠP CHIẾU PHIM&#xa;(CINESTAR CINEMA SYSTEM)" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;fontStyle=1;fontSize=14;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="540" y="40" width="560" height="70" as="geometry" />
        </mxCell>
        <mxCell id="mod1" value="1.0 PHÂN HỆ KHÁCH HÀNG" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;fontStyle=1;fontSize=12;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="120" y="170" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="mod2" value="2.0 PHÂN HỆ NHÂN VIÊN" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;fontStyle=1;fontSize=12;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="470" y="170" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="mod3" value="3.0 PHÂN HỆ QUẢN LÝ" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;fontStyle=1;fontSize=12;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="820" y="170" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="mod4" value="4.0 PHÂN HỆ QUẢN TRỊ" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;fontStyle=1;fontSize=12;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="1170" y="170" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="edge_root" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;endArrow=none;" edge="1" parent="1" source="root_node">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="820" y="140" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="edge_bus" value="" style="endArrow=none;html=1;rounded=0;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="260" y="140" as="sourcePoint" />
            <mxPoint x="1310" y="140" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="edge_m1" value="" style="endArrow=none;html=1;rounded=0;strokeColor=#000000;strokeWidth=1.5;" edge="1" parent="1" target="mod1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="260" y="140" as="sourcePoint" />
            <mxPoint x="260" y="170" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="edge_m2" value="" style="endArrow=none;html=1;rounded=0;strokeColor=#000000;strokeWidth=1.5;" edge="1" parent="1" target="mod2">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="610" y="140" as="sourcePoint" />
            <mxPoint x="610" y="170" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="edge_m3" value="" style="endArrow=none;html=1;rounded=0;strokeColor=#000000;strokeWidth=1.5;" edge="1" parent="1" target="mod3">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="960" y="140" as="sourcePoint" />
            <mxPoint x="960" y="170" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="edge_m4" value="" style="endArrow=none;html=1;rounded=0;strokeColor=#000000;strokeWidth=1.5;" edge="1" parent="1" target="mod4">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1310" y="140" as="sourcePoint" />
            <mxPoint x="1310" y="170" as="targetPoint" />
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

with open(os.path.join(drawio_dir, 'FDD_phan_cap_chuc_nang.drawio'), 'w', encoding='utf-8') as f:
    f.write(fdd_xml)

# 2. UseCase Tong Quat Draw.io XML
uc_xml = """<mxfile host="app.diagrams.net" modified="2026-10-13T16:00:00.000Z" agent="Antigravity" version="24.0.0">
  <diagram id="UC_General" name="Biểu đồ Use Case tổng quát">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="sys_boundary" value="HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU CINESTAR" style="shape=rect;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fontSize=14;strokeColor=#000000;fillColor=#ffffff;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="380" y="60" width="860" height="980" as="geometry" />
        </mxCell>
        <mxCell id="act_client" value="Khách hàng&#xa;(Client)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;strokeColor=#000000;fillColor=#ffffff;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="200" y="240" width="50" height="100" as="geometry" />
        </mxCell>
        <mxCell id="act_staff" value="Nhân viên quầy&#xa;(Staff)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;strokeColor=#000000;fillColor=#ffffff;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="200" y="680" width="50" height="100" as="geometry" />
        </mxCell>
        <mxCell id="act_mgr" value="Quản lý rạp&#xa;(Manager)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;strokeColor=#000000;fillColor=#ffffff;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1380" y="240" width="50" height="100" as="geometry" />
        </mxCell>
        <mxCell id="act_adm" value="Quản trị viên&#xa;(Admin)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;strokeColor=#000000;fillColor=#ffffff;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1380" y="680" width="50" height="100" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

with open(os.path.join(drawio_dir, 'UseCase_tong_quat.drawio'), 'w', encoding='utf-8') as f:
    f.write(uc_xml)

# 3. ERD Draw.io XML
erd_xml = """<mxfile host="app.diagrams.net" modified="2026-10-13T16:00:00.000Z" agent="Antigravity" version="24.0.0">
  <diagram id="ERD_Diagram" name="Sơ đồ quan hệ thực thể ERD chuẩn hóa 3NF">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="title" value="SƠ ĐỒ QUAN HỆ THỰC THỂ (ERD) CHUẨN HÓA 3NF - CINEMA STAR" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="500" y="20" width="650" height="40" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

with open(os.path.join(drawio_dir, 'ERD_database_3NF.drawio'), 'w', encoding='utf-8') as f:
    f.write(erd_xml)

print("Created Draw.io XML files in report_assets/drawio/")
