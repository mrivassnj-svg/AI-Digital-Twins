# -*- coding: utf-8 -*-
"""Generate six conceptual isometric technical-design plates for ITAI 4371.

Install: python -m pip install numpy matplotlib
Run:     python digital_twin_technical_plates.py
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch
import matplotlib.colors as mcolors

plt.rcdefaults()
plt.rcParams.update({"font.family":"DejaVu Sans","figure.dpi":160,"savefig.dpi":300,"figure.autolayout":False})

BG="#DCEBF0"; INK="#263238"; MID="#66757B"; LIGHT="#AAB8BD"; PALE="#EEF5F7"; CONCRETE="#8D9699"; DARK="#667176"
STEEL="#56636A"; GLASS="#AECBD6"; BLUE="#168EAE"; GREEN="#46966A"; AMBER="#D58A25"; RED="#C9574E"; PURPLE="#7460A8"
W=16; H=10


def iso(x,y,z,angle=30):
    r=np.radians(angle)
    return (x-y)*np.cos(r),(x+y)*np.sin(r)+z


def polygon_iso(ax, pts, fc=CONCRETE, ec=INK, lw=.65, alpha=1, zorder=2):
    pts=np.asarray(pts); u,v=iso(pts[:,0],pts[:,1],pts[:,2])
    ax.add_patch(Polygon(np.column_stack([u,v]),closed=True,fc=fc,ec=ec,lw=lw,alpha=alpha,zorder=zorder))
    return u,v


def box(ax,x,y,z,dx,dy,dz,fc=CONCRETE,ec=INK,lw=.65,alpha=1,zorder=2):
    p=np.array([[x,y,z],[x+dx,y,z],[x+dx,y+dy,z],[x,y+dy,z],[x,y,z+dz],[x+dx,y,z+dz],[x+dx,y+dy,z+dz],[x,y+dy,z+dz]])
    faces=[[0,1,2,3],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7],[4,5,6,7]]
    base=np.array(mcolors.to_rgb(fc)); shades=[.75,.92,.80,.70,.85,1.0]
    for face,shade in zip(faces,shades): polygon_iso(ax,p[face],fc=np.clip(base*shade,0,1),ec=ec,lw=lw,alpha=alpha,zorder=zorder)


def line_iso(ax, points, color=INK, lw=.6, ls="-", alpha=1, zorder=5):
    p=np.asarray(points); u,v=iso(p[:,0],p[:,1],p[:,2]); ax.plot(u,v,color=color,lw=lw,ls=ls,alpha=alpha,zorder=zorder)
    return u,v


def point_iso(x,y,z): return iso(x,y,z)


def canvas(title, subtitle, model_no, tier, subject):
    fig,ax=plt.subplots(figsize=(W,H),dpi=160,facecolor=BG)
    ax.set_facecolor(BG); ax.axis("off"); ax.set_xlim(-86,86); ax.set_ylim(-58,58)
    ax.plot([-84,84],[53,53],color=INK,lw=.6); ax.plot([-84,84],[-53,-53],color=MID,lw=.4)
    ax.text(-83,55.2,f"{subject.upper()}  /  TECHNICAL MODEL",fontsize=6.5,color=INK,weight="bold",va="bottom")
    ax.text(-83,51.4,title.upper(),fontsize=8.4,color=INK,weight="bold",va="bottom")
    ax.text(-83,47.8,subtitle.upper(),fontsize=5.2,color=MID,va="bottom")
    ax.text(81,55.2,"ISO",fontsize=5.2,color=MID,ha="right",va="bottom")
    ax.text(81,51.4,f"MODEL {int(model_no):02d}",fontsize=5.2,color=MID,ha="right",va="bottom")
    ax.text(81,47.8,tier.upper(),fontsize=5.2,color=MID,ha="right",va="bottom")
    return fig,ax


def ground_grid(ax, extent=46, step=5, z=-12):
    for c in range(-extent,extent+1,step):
        line_iso(ax,np.array([[c,-extent,z],[c,extent,z]]),color="#B8CED5",lw=.32,alpha=.7,zorder=0)
        line_iso(ax,np.array([[-extent,c,z],[extent,c,z]]),color="#B8CED5",lw=.32,alpha=.7,zorder=0)


def leader(ax, anchor, text, offset=(12,8), color=INK):
    u,v=point_iso(*anchor); tx,ty=u+offset[0],v+offset[1]
    ax.annotate(text,xy=(u,v),xytext=(tx,ty),fontsize=5,color=color,weight="bold",ha="center",va="center",
                bbox=dict(boxstyle="round,pad=.18",fc=PALE,ec=color,lw=.4,alpha=.96),
                arrowprops=dict(arrowstyle="-",color=color,lw=.55))


def dimension(ax, p1, p2, text, offset=(0,-5)):
    u1,v1=point_iso(*p1); u2,v2=point_iso(*p2); dx,dy=offset
    ax.plot([u1,u2],[v1,v2],color=MID,lw=.45); ax.plot([u1+dx,u1+dx],[v1+dy,v1+dy],color=MID,lw=.4); ax.plot([u2+dx,u2+dx],[v2+dy,v2+dy],color=MID,lw=.4)
    ax.text((u1+u2)/2+dx,(v1+v2)/2+dy,text,fontsize=4.6,color=MID,ha="center",va="center")


def title_block(ax, model_no, system, tier, legend):
    x0,y0=51,-50
    ax.add_patch(Rectangle((x0,y0),31,12,fc="#EAF2F5",ec=MID,lw=.5,zorder=20))
    ax.text(x0+1,y0+9.7,"ITAI 4371 | CONCEPTUAL DIGITAL TWIN",fontsize=4.5,color=INK,weight="bold")
    ax.text(x0+1,y0+7.3,system,fontsize=4.2,color=INK)
    ax.text(x0+1,y0+4.9,f"MODEL {model_no:02d}  |  {tier}",fontsize=4.1,color=MID)
    ax.text(x0+1,y0+2.3,legend,fontsize=3.7,color=MID)
    ax.text(x0+29.5,y0+1.0,"CONCEPTUAL",fontsize=3.8,color=MID,ha="right")


def footer_note(ax, note):
    ax.text(-83,-50,note,fontsize=4.2,color=MID,ha="left",va="center")


def finish(fig, ax, filename):
    ax.set_aspect("equal",adjustable="box")
    fig.savefig(filename,dpi=300,facecolor=BG,bbox_inches=None,pad_inches=.04)
    plt.close(fig)
    return Path(filename)


def plate_01(out):
    fig,ax=canvas("Autodesk Descriptive Twin","Isometric Structural BIM / IFC Concept","1","Tier 1 — Static Geometry","Multi-story steel-frame building")
    ground_grid(ax)
    box(ax,-28,-24,-12,56,48,2,fc="#B3BABD",ec=INK,lw=.8)
    for z in [-8,3,14]: box(ax,-26,-22,z,52,44,1.8,fc="#AAB1B4",ec=STEEL,lw=.55,alpha=.92)
    box(ax,-9,-8,-10,18,16,28,fc="#788287",ec=INK,lw=.8)
    for x in [-24,-8,8,24]:
        for y in [-20,-6,8,20]: line_iso(ax,[[x,y,-10],[x,y,17]],color=STEEL,lw=1.0,zorder=12)
    for y in [-20,-6,8,20]: line_iso(ax,[[-24,y,17],[24,y,17]],color=STEEL,lw=.65,zorder=12)
    for x in [-24,24]:
        line_iso(ax,[[x,-20,-8],[x,-6,14]],color=MID,lw=.55); line_iso(ax,[[x,-6,-8],[x,-20,14]],color=MID,lw=.55)
    line_iso(ax,[[-20,-16,1],[-20,16,1],[20,16,1],[20,-16,1],[-20,-16,1]],color=BLUE,lw=1.35,ls="-.",zorder=15)
    leader(ax,(-24,-20,16),"STEEL COLUMN GRID",(-13,8)); leader(ax,(0,0,17),"SHEAR-WALL CORE",(13,7)); leader(ax,(20,16,1),"STATIC MEP TRUNK",(13,-4),BLUE)
    dimension(ax,(-28,-24,-12),(28,-24,-12),"CONCEPTUAL 56M STRUCTURAL BAY",(0,-7))
    footer_note(ax,"STATIC GEOMETRY ONLY — NO LIVE LOAD, VIBRATION, OR ENERGY TELEMETRY CONNECTED")
    title_block(ax,1,"BIM STRUCTURAL ASSET","LOW VERISIMILITUDE","Steel / Slabs / Core / MEP")
    return finish(fig,ax,out/"01_autodesk_bim_technical_model.png")


def plate_02(out):
    fig,ax=canvas("Minute Maid Park","Conceptual Isometric Stadium / Retractable-Roof Study","2","Tier 1 — Static Geometry","Houston ballpark")
    ground_grid(ax,52)
    box(ax,-39,-34,-12,78,68,2,fc="#B7BEC0",ec=INK,lw=.75)
    theta=np.linspace(np.radians(15),np.radians(165),100)
    for r,z in [(27,-6),(32,-2),(37,2),(41,6)]:
        x=r*np.cos(theta); y=r*np.sin(theta)
        line_iso(ax,np.column_stack([x,y,np.full_like(x,z)]),color=STEEL,lw=1.1,zorder=8)
        if r>27:
            x2=(r-3)*np.cos(theta); y2=(r-3)*np.sin(theta)
            line_iso(ax,np.column_stack([x2,y2,np.full_like(x2,z-2)]),color=LIGHT,lw=.55,zorder=7)
    field=np.array([[0,-19,-7],[18,-1,-7],[0,18,-7],[-18,-1,-7]])
    polygon_iso(ax,field,fc="#86A989",ec=INK,lw=.75,zorder=6)
    for yy in [10,31]: line_iso(ax,[[-32,yy,15],[32,yy,15]],color=STEEL,lw=.8,ls="--",zorder=14)
    for i,(x0,x1) in enumerate([(-31,-11),(-9,11),(13,33)]):
        box(ax,x0,10,16,x1-x0,20,2.8,fc=["#858E91","#929A9D","#7A8589"][i],ec=INK,lw=.7,zorder=16)
        line_iso(ax,[[x0,10,18.9],[x1,30,18.9]],color=INK,lw=.45,zorder=18); line_iso(ax,[[x1,10,18.9],[x0,30,18.9]],color=INK,lw=.45,zorder=18)
    box(ax,-40,3,-8,11,31,20,fc="#A0A8AB",ec=INK,lw=.7,zorder=9)
    box(ax,29,3,-8,11,31,20,fc="#A0A8AB",ec=INK,lw=.7,zorder=9)
    for x in [-29,-10,12,33]: line_iso(ax,[[x,10,15],[x,30,19]],color=INK,lw=.5,zorder=18)
    leader(ax,(0,20,19),"THREE-PANEL\nRETRACTABLE ROOF",(17,7)); leader(ax,(33,10,15),"RAIL-MOUNTED\nTRUSS EDGE",(17,-4)); leader(ax,(-35,18,7),"LEFT-FIELD\nMASSING",(-15,4)); leader(ax,(0,0,-7),"FIELD / BOWL\nGEOMETRY",(13,-10),GREEN)
    dimension(ax,(-39,-34,-12),(39,-34,-12),"CONCEPTUAL 78M BALLPARK ENVELOPE",(0,-8))
    footer_note(ax,"CONCEPTUAL ARCHITECTURAL STUDY — ROOF POSITION, CROWD, AND WEATHER STATES ARE NOT LIVE")
    title_block(ax,2,"BALLPARK STRUCTURE","LOW VERISIMILITUDE","Bowl / Roof Panels / Rails / Field")
    return finish(fig,ax,out/"02_minute_maid_technical_model.png")


def plate_03(out):
    fig,ax=canvas("Charles H. Wright Museum","Ford Freedom Rotunda / Instrumented Dome Study","3","Tier 2 — Connected Monitoring","Detroit museum")
    ground_grid(ax,42)
    box(ax,-34,-25,-11,68,50,2,fc="#B7BEC0",ec=INK,lw=.75)
    box(ax,-33,-9,-9,20,18,7,fc="#9BA4A7",ec=INK,lw=.65); box(ax,13,-9,-9,20,18,7,fc="#9BA4A7",ec=INK,lw=.65); box(ax,-13,-28,-9,26,17,7,fc="#9BA4A7",ec=INK,lw=.65)
    th=np.linspace(0,2*np.pi,72)
    for phi in np.linspace(0,np.pi/2,10):
        r=20*np.cos(phi); z=-2+20*np.sin(phi)
        line_iso(ax,np.column_stack([r*np.cos(th),r*np.sin(th),np.full_like(th,z)]),color=BLUE,lw=.5,alpha=.85,zorder=10)
    for ang in np.linspace(0,2*np.pi,16,endpoint=False):
        p=np.linspace(0,np.pi/2,28); line_iso(ax,np.column_stack([20*np.cos(p)*np.cos(ang),20*np.cos(p)*np.sin(ang),-2+20*np.sin(p)]),color=STEEL,lw=.65,zorder=11)
    for x,y,z,label,off in [(0,0,15,"CO₂ SENSOR\nILLUSTRATIVE",(12,5)),(-18,0,-2,"TEMP SENSOR\nILLUSTRATIVE",(-13,4)),(18,0,-2,"RH SENSOR\nILLUSTRATIVE",(13,4)),(0,-18,-2,"LUX SENSOR\nILLUSTRATIVE",(0,-8))]:
        u,v=point_iso(x,y,z); ax.plot(u,v,marker="o",ms=5,color=GREEN,markeredgecolor=INK,zorder=30); leader(ax,(x,y,z),label,off,GREEN)
    leader(ax,(0,0,18),"GLASS DOME\nRIB NETWORK",(-14,9)); leader(ax,(-24,0,-3),"WEST GALLERY\nVOLUME",(-12,-3)); leader(ax,(0,-20,-3),"ARCHIVE /\nCOLLECTIONS",(12,-6))
    dimension(ax,(-20,0,-2),(20,0,-2),"CONCEPTUAL 40M ROTUNDA DIAMETER",(0,-8))
    footer_note(ax,"CONNECTED MONITORING CONCEPT — DEVICE PLACEMENT AND READINGS ARE ILLUSTRATIVE")
    title_block(ax,3,"ROTUNDA ENVIRONMENT","MEDIUM VERISIMILITUDE","Dome / Galleries / CO₂ / RH / Lux")
    return finish(fig,ax,out/"03_wright_museum_technical_model.png")


def plate_04(out):
    fig,ax=canvas("George R. Brown Convention Center","Contiguous Multi-Hall / Concourse Operations Study","4","Tier 2 — Connected Monitoring","Houston convention facility")
    ground_grid(ax,52)
    box(ax,-46,-29,-12,92,58,2,fc="#B6BEC0",ec=INK,lw=.75)
    box(ax,-42,-6,-9,84,30,18,fc="#929B9E",ec=INK,lw=.75,alpha=.9)
    box(ax,-42,-12,-4,84,6,7,fc=GLASS,ec=BLUE,lw=.6,alpha=.75,zorder=12)
    for x,name in [(-42,"A"),(-25,"B"),(-8,"C"),(9,"D"),(26,"E")]:
        line_iso(ax,[[x,-6,-9],[x,24,-9],[x,24,9]],color=INK,lw=.6,zorder=14)
        u,v=point_iso(x+8,8,10); ax.text(u,v,f"HALL {name}",fontsize=5,color=PALE,ha="center",weight="bold",zorder=15)
        u,v=point_iso(x+8,8,11); ax.plot(u,v,marker="o",ms=4.5,color=GREEN,zorder=18)
    for x in [-34,-17,0,17,34]:
        box(ax,x,-6,9,4,4,8,fc="#9B4A43",ec=INK,lw=.55,zorder=16)
    polygon_iso(ax,np.array([[-42,-28,-10],[-20,-28,-10],[-20,-15,-10],[-42,-15,-10]]),fc=BLUE,ec=INK,lw=.55,alpha=.72)
    box(ax,-32,-17,-2,9,7,3,fc=GLASS,ec=BLUE,lw=.55,zorder=16)
    leader(ax,(-35,-9,3),"GLAZED CONCOURSE\nSPINE",(-14,8),BLUE); leader(ax,(0,10,10),"HALL SUBMETER\nILLUSTRATIVE",(12,7),GREEN); leader(ax,(28,-4,14),"MECHANICAL\nCORE",(14,4)); leader(ax,(-31,-22,-9),"PLAZA / WATER\nEDGE",(-14,-3),BLUE)
    dimension(ax,(-42,-6,-9),(42,-6,-9),"CONCEPTUAL 84M CONTIGUOUS EXHIBIT AXIS",(0,-8))
    footer_note(ax,"CONNECTED FACILITY CONCEPT — HALL OCCUPANCY, ENERGY, AND HVAC VALUES ARE ILLUSTRATIVE")
    title_block(ax,4,"CONVENTION OPERATIONS","MEDIUM VERISIMILITUDE","Halls / Concourse / Meters / HVAC")
    return finish(fig,ax,out/"04_grb_convention_center_technical_model.png")


def plate_05(out):
    fig,ax=canvas("NASA National Airspace System","Airspace Sector / Storm-Conflict Simulation Study","5","Tier 3 — Predictive Simulation","4D airspace model")
    ground_grid(ax,48,z=-15)
    corners=np.array([[-38,-28,-12],[38,-28,-12],[38,28,-12],[-38,28,-12]])
    polygon_iso(ax,corners,fc="#C6D7DC",ec=MID,lw=.55,alpha=.35,zorder=1)
    for z in [-12,2,16,30]:
        line_iso(ax,[[-38,-28,z],[38,-28,z],[38,28,z],[-38,28,z],[-38,-28,z]],color=MID,lw=.45,ls="--",alpha=.75)
    for x,y in [(-38,-28),(38,-28),(38,28),(-38,28)]: line_iso(ax,[[x,y,-12],[x,y,30]],color=MID,lw=.45,ls=":")
    th=np.linspace(0,2*np.pi,50)
    for z,r,col,al in [(-8,13,"#D89088",.22),(5,11,"#CF6E63",.26),(18,8,"#B83D37",.32)]:
        polygon_iso(ax,np.column_stack([12+r*np.cos(th),5+r*np.sin(th),np.full_like(th,z)]),fc=col,ec=RED,lw=.55,alpha=al,zorder=8)
    for ang in np.linspace(0,2*np.pi,10,endpoint=False): line_iso(ax,[[12,5,-8],[12+8*np.cos(ang),5+8*np.sin(ang),18]],color=RED,lw=.35,alpha=.6,zorder=9)
    line_iso(ax,[[-32,-21,7],[-8,-7,7],[12,5,7],[31,19,7]],color=RED,lw=1.1,ls="--",zorder=12)
    t=np.linspace(0,1,60); x=(1-t)**2*(-32)+2*(1-t)*t*(-2)+t**2*31; y=(1-t)**2*(-21)+2*(1-t)*t*(-24)+t**2*19; z=np.full_like(t,7)
    line_iso(ax,np.column_stack([x,y,z]),color=AMBER,lw=2.0,zorder=14)
    k=29; u,v=point_iso(x[k],y[k],z[k]); ax.plot(u,v,marker="^",ms=8,color=BLUE,markeredgecolor=INK,zorder=20)
    leader(ax,(x[k],y[k],z[k]),"AIRCRAFT TRACK\nILLUSTRATIVE",(-15,8),BLUE); leader(ax,(12,5,18),"CONVECTIVE CELL\nFORECAST VOLUME",(14,6),RED); leader(ax,(-8,-7,7),"NOMINAL ROUTE\nBLOCKED",(-14,-5),RED); leader(ax,(0,-18,7),"SOLVER REROUTE\nSEPARATION PATH",(13,-4),AMBER)
    dimension(ax,(-38,-28,-12),(38,-28,-12),"CONCEPTUAL ARTCC SECTOR WIDTH",(0,-8))
    footer_note(ax,"PREDICTIVE SIMULATION CONCEPT — AIRCRAFT IDENTITIES, TRACKS, AND WEATHER VALUES ARE ILLUSTRATIVE")
    title_block(ax,5,"AIRSPACE CONFLICT SOLVER","HIGH VERISIMILITUDE","Sector / Weather / Track / Reroute")
    return finish(fig,ax,out/"05_nasa_airspace_technical_model.png")


def plate_06(out):
    fig,ax=canvas("Buffalo Bayou Hydrology Twin","Terrain Mesh / Reservoir Controls / CFD Inundation Study","6","Tier 3 — Predictive Simulation","Houston watershed model")
    gx=np.linspace(-43,43,22); gy=np.linspace(-28,28,18); GX,GY=np.meshgrid(gx,gy); GZ=-12+.006*(GX**2+GY**2)-3*np.exp(-(GY-4*np.sin(GX/7))**2/30)
    for i in range(len(gx)): line_iso(ax,np.column_stack([GX[:,i],GY[:,i],GZ[:,i]]),color="#9EBAC3",lw=.33,alpha=.8,zorder=1)
    for j in range(len(gy)): line_iso(ax,np.column_stack([GX[j,:],GY[j,:],GZ[j,:]]),color="#9EBAC3",lw=.33,alpha=.8,zorder=1)
    bx=np.linspace(-36,40,130); by=4*np.sin(bx/7)+1.5*np.sin(bx/3.5); bz=-11.5*np.ones_like(bx)
    pu,pv=iso(bx,by+10,bz+2.5); qu,qv=iso(bx,by-10,bz+2.5); ax.fill(np.append(pu,qu[::-1]),np.append(pv,qv[::-1]),color=RED,alpha=.22,zorder=3)
    pu,pv=iso(bx,by+5,bz+1.1); qu,qv=iso(bx,by-5,bz+1.1); ax.fill(np.append(pu,qu[::-1]),np.append(pv,qv[::-1]),color=AMBER,alpha=.25,zorder=4)
    line_iso(ax,np.column_stack([bx,by,bz]),color=BLUE,lw=2.8,zorder=10)
    for x,y,name in [(-31,16,"ADDICKS\nCONTROL"),(-31,-17,"BARKER\nCONTROL")]:
        box(ax,x-5,y-3,-7,10,6,7,fc="#7C78A7",ec=INK,lw=.65,zorder=14); leader(ax,(x,y,0),name,(12,4),PURPLE)
    for x in [-18,4,27]:
        y=4*np.sin(x/7)+1.5*np.sin(x/3.5); u,v=point_iso(x,y,-11); ax.plot(u,v,marker="^",ms=7,color=AMBER,markeredgecolor=INK,zorder=20); leader(ax,(x,y,-11),"USGS GAUGE\nILLUSTRATIVE",(8,7),AMBER)
    for x in [-5,16,33]:
        y=4*np.sin(x/7)+1.5*np.sin(x/3.5); line_iso(ax,[[x-3,y-2,-9],[x+3,y+2,-9]],color=INK,lw=.85,zorder=15)
    leader(ax,(10,0,-9),"+12H INUNDATION\nENVELOPE",(17,7),RED); leader(ax,(16,4*np.sin(16/7)+1.5*np.sin(16/3.5),-11),"CFD CHANNEL\nCENTERLINE",(14,-5),BLUE)
    dimension(ax,(-40,-25,-12),(40,-25,-12),"CONCEPTUAL MODEL REACH",(0,-8))
    footer_note(ax,"PREDICTIVE HYDROLOGY CONCEPT — GATE FLOWS, GAUGE STAGES, AND INUNDATION EXTENTS ARE ILLUSTRATIVE")
    title_block(ax,6,"HYDRODYNAMIC CFD TWIN","HIGH VERISIMILITUDE","Terrain / Gauges / Gates / Floodplain")
    return finish(fig,ax,out/"06_buffalo_bayou_technical_model.png")


def index_plate(out, files):
    fig,ax=plt.subplots(figsize=(W,H),dpi=160,facecolor=BG); ax.set_facecolor(BG); ax.axis("off"); ax.set_xlim(0,100); ax.set_ylim(0,100)
    ax.text(5,94,"ITAI 4371 — CONCEPTUAL DIGITAL TWIN TECHNICAL-PLATE SET",fontsize=13,color=INK,weight="bold")
    ax.text(5,89,"Six subject plates: static geometry → connected monitoring → predictive simulation",fontsize=7,color=MID)
    entries=[("01","Autodesk BIM","Static Geometry","LOW",MID),("02","Minute Maid Park","Static Geometry","LOW",MID),("03","Wright Museum","Environmental Monitoring","MEDIUM",BLUE),("04","GRB Convention Center","Operations Monitoring","MEDIUM",BLUE),("05","NASA Airspace","Conflict Simulation","HIGH",PURPLE),("06","Buffalo Bayou","Hydrodynamic Simulation","HIGH",PURPLE)]
    for i,(n,title,desc,tier,col) in enumerate(entries):
        c=i%2; r=i//2; x=7+c*47; y=70-r*22
        ax.add_patch(Rectangle((x,y),40,16,fc=PALE,ec=col,lw=1))
        ax.text(x+3,y+11.5,f"{n}  {title}",fontsize=8,color=INK,weight="bold")
        ax.text(x+3,y+7,desc,fontsize=5.8,color=MID)
        ax.text(x+3,y+3,f"TIER: {tier}",fontsize=5.2,color=col,weight="bold")
    ax.text(5,8,"All plates are conceptual assignment visualizations. Landmark-inspired features do not constitute surveyed, engineered, or live operational models.",fontsize=5.2,color=MID)
    ax.plot([5,95],[5,5],color=MID,lw=.5)
    path=out/"00_digital_twin_matrix_index.png"; fig.savefig(path,dpi=300,facecolor=BG,bbox_inches=None,pad_inches=.04); plt.close(fig); return path


def main():
    out=Path("technical_plates"); out.mkdir(exist_ok=True)
    files=[plate_01(out),plate_02(out),plate_03(out),plate_04(out),plate_05(out),plate_06(out)]
    files.insert(0,index_plate(out,files))
    missing=[p for p in files if not p.exists() or p.stat().st_size<50000]
    if missing: raise RuntimeError("Verification failed: " + ", ".join(map(str,missing)))
    print("[OK] Created and verified technical plates:")
    for p in files: print(f"  {p.resolve()} ({p.stat().st_size:,} bytes)")

if __name__=="__main__": main()
