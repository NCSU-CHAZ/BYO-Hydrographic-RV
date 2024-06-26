from process_file_HydroSurveyor import Hydro_process, dtnum_dttime, dtnum_dttime_adcp
import matplotlib.pyplot as plt
from read_HydroSurveyor import create_df
import numpy as np
from process_session_HydroSurveyor import Hydro_session_process
import datetime as dt
import pandas as pd
from scipy.signal import medfilt


Data = Hydro_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520_raw.mat"
)

AdcpData, info = create_df(
    r"c:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\CMS52002_L0.mat"
)
del info

AutoData = Hydro_session_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520.mat"
)

LayerData = pd.read_csv(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Velocity_Vectors.csv",
    header=0,
)
DateTime = pd.to_datetime(LayerData["utc_time"], format="%Y-%m-%d %H:%M:%S.%f")
tos = dt.timedelta(hours=4)
DateTime = DateTime - tos


# MatVel,info = create_df(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\HydroAnalysisExp.mat"); del info


def raw_comparison_plot(Data):
    raw_velE = np.nanmean(Data["EastVel"], axis=1)
    raw_velN = np.nanmean(Data["NorthVel"], axis=1)
    raw_velU = np.nanmean(Data["VertVel"], axis=1)

    plt.figure()
    plt.plot(Data["DateTime"], raw_velE, label="Easting")
    plt.plot(Data["DateTime"], raw_velN, label="Northing")
    plt.plot(Data["DateTime"], raw_velU, label="Vertical")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Raw Velocities vs Time ~~File~~")
    plt.legend()
    plt.show()


def BT_comparison_plot(Data):
    heading_rad = np.deg2rad(AutoData["HydroSurveyor_MagneticHeading_deg"])
    heading_rad = heading_rad.values.reshape(-1, 1)

    BtVelN = AutoData["BtVelX"] * np.cos(heading_rad) + AutoData["BtVelY"] * np.sin(
        heading_rad
    )

    plt.figure()
    plt.plot(Data["DateTime"], Data["BtVel"].iloc[:, 1], label="File")
    plt.plot(AutoData["DateTime"], BtVelN, label="Session")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Bottom Track Velocities vs Time")
    plt.legend()
    plt.show()


def auto_manual_comparison(AutoData, Data):
    auto_velN = np.nanmean(AutoData["NorthVel"], axis=1)
    int_velN = np.nanmean(Data["NorthVel_interp"], axis=1)
    fig, axs = plt.subplots(2)
    axs[0].plot(Data["DateTime"], int_velN, color="green", label="File Processing")
    axs[1].plot(AutoData["DateTime"], auto_velN, label="Session Processing")
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Velocity (m/s)")
    fig.suptitle("Northing Velocities vs Time")
    fig.legend()
    plt.show()


def depth_velocity_plot(Data):
    fig, axs = plt.subplots(3)

    im1 = axs[0].pcolormesh(
        Data["DateTime"],
        Data["interpCellDepth"],
        Data["EastVel_interp"].T,
        vmin=np.nanmin(Data["EastVel_interp"]),
        vmax=np.nanmax(Data["EastVel_interp"]),
        shading="auto",
    )
    im2 = axs[1].pcolormesh(
        Data["DateTime"],
        Data["interpCellDepth"],
        Data["NorthVel_interp"].T,
        vmin=np.nanmin(Data["NorthVel_interp"]),
        vmax=np.nanmax(Data["NorthVel_interp"]),
        shading="auto",
    )
    im3 = axs[2].pcolormesh(
        Data["DateTime"],
        Data["interpCellDepth"],
        Data["VertVel_interp"].T,
        vmin=np.nanmin(Data["VertVel_interp"]),
        vmax=np.nanmax(Data["VertVel_interp"]),
        shading="auto",
    )
    axs[0].plot(Data["DateTime"], Data["VbDepth_m"])
    axs[1].plot(Data["DateTime"], Data["VbDepth_m"])
    axs[2].plot(Data["DateTime"], Data["VbDepth_m"])

    axs[0].set_title("Easting Velocity")
    axs[1].set_title("Northing Velocity")
    axs[2].set_title("Vertical Velocity")
    cb1 = fig.colorbar(im1, ax=axs[0])
    cb2 = fig.colorbar(im2, ax=axs[1])
    cb3 = fig.colorbar(im3, ax=axs[2])
    cb1.ax.set_ylabel("Velocity (m/s)")
    cb2.ax.set_ylabel("Velocity (m/s)")
    cb3.ax.set_ylabel("Velocity (m/s)")
    fig.tight_layout()
    fig.supxlabel("DateTime (DD HH:MM)")
    fig.supylabel("Depth (m)")
    plt.show()


def adcp_comparison(AdcpData, Data, AutoData, LayerData):
    lw = 1
    plt.figure()
    plt.plot(
        dtnum_dttime_adcp(AdcpData["date"]),
        np.nanmean(AdcpData["VelNorth"], axis=0),
        label="ADCP Data",
    )
    plt.plot(
        Data["DateTime"],
        medfilt(np.nanmean(Data["NorthVel_interp"], axis=1)),
        color="Red",
        label="File Data",
        linewidth=lw,
    )
    plt.plot(
        AutoData["DateTime"],
        medfilt(np.nanmean(AutoData["NorthVel"], axis=1)),
        label="Session Data",
        color="Green",
        linewidth=lw,
    )
    plt.plot(DateTime, medfilt(LayerData["average_N"]), label="Layer", linewidth=lw)
    plt.xlim(AutoData["DateTime"][0], AutoData["DateTime"][-1])
    plt.title("Northing Velocities vs Time")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.show()


def Snr_plot(AutoData):
    plt.figure()
    plt.plot(AutoData["ADP_snr"][0][100])
    plt.title("ADP Signal to Noise ")
    plt.xlabel("Cell Number")
    plt.ylabel("Signal to Noise Ratio")
    plt.show()


def ADCP_Data(AdcpData):
    plt.figure()
    plt.plot(
        dtnum_dttime_adcp(AdcpData["date"]),
        np.nanmean(AdcpData["VelNorth"], axis=0),
        label="ADCP Data",
    )
    plt.axvline(x=AutoData["DateTime"][0], color="red", label="Start of first session")
    plt.axvline(x=AutoData["DateTime"][-1], color="red", label="End of first session")
    plt.title("Aquadopp Velocity versus Time")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.show()


# raw_comparison_plot(Data)

# BT_comparison_plot(Data)

# auto_manual_comparison(AutoData, Data)

# depth_velocity_plot(Data)

# adcp_comparison(AdcpData, Data, AutoData, LayerData)

# Snr_plot(AutoData)

#ADCP_Data(AdcpData)
