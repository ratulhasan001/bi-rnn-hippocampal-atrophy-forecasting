import os
import pandas as pd
import matplotlib.pyplot as plt
from nilearn import plotting


# === 1. CONFIGURATION ===
ROOT_DIR = "/content/drive/MyDrive/ADNI_dataset/ADNI"
DATA_CSV = "final_dataset_split.csv"
VOL_CSV  = "/content/drive/MyDrive/ADNI_dataset/hippocampal_volumes.csv"


def generate_1x3_flowchart_brains():
    if not os.path.exists(DATA_CSV) or not os.path.exists(VOL_CSV):
        print("❌ Missing CSV files. Check your paths.")
        return

    # === 2. LOAD DATA ===
    df_data = pd.read_csv(DATA_CSV)
    df_vol  = pd.read_csv(VOL_CSV)
    df = pd.merge(df_data, df_vol, on=['SubjectID', 'Visit', 'Diagnosis'], how='inner')
    df_bl = df[df['Visit'].str.lower().isin(['bl', 'sc'])]

    # === 3. SELECT ONE PERFECT SUBJECT PER CLASS ===
    cn_cands  = df_bl[(df_bl['Diagnosis'] == 'CN')  & (df_bl['Volume_mm3'].between(7400, 8200))]
    mci_cands = df_bl[(df_bl['Diagnosis'] == 'MCI') & (df_bl['Volume_mm3'].between(5800, 6500))]
    ad_cands  = df_bl[(df_bl['Diagnosis'] == 'AD')  & (df_bl['Volume_mm3'].between(3500, 4800))]

    selected_subjects = {
        'CN':  cn_cands.iloc[0]  if not cn_cands.empty  else df_bl[df_bl['Diagnosis'] == 'CN'].iloc[0],
        'MCI': mci_cands.iloc[0] if not mci_cands.empty else df_bl[df_bl['Diagnosis'] == 'MCI'].iloc[0],
        'AD':  ad_cands.iloc[0]  if not ad_cands.empty  else df_bl[df_bl['Diagnosis'] == 'AD'].iloc[0],
    }

    # === 4. SETUP FIGURE ===
    # FIX 1: Use gridspec_kw to give the brain axes extra bottom padding for the text row
    fig = plt.figure(figsize=(15, 7.5), facecolor='black')

    # Each column has two rows: brain image (height 5) + text row (height 1)
    from matplotlib.gridspec import GridSpec
    gs = GridSpec(
        nrows=2, ncols=3,
        height_ratios=[5, 1],       # top row = brain, bottom row = volume text
        hspace=0.05,                # minimal gap between brain and text row
        wspace=0.08,
        figure=fig
    )

    print("Generating 1x3 zoomed brains with fixed label spacing...")

    classes = ['CN', 'MCI', 'AD']
    class_colors = {'CN': '#00CC66', 'MCI': '#FFD700', 'AD': '#FF4444'}

    for col_idx, cls in enumerate(classes):
        row = selected_subjects[cls]

        # Brain axes (top row)
        ax_brain = fig.add_subplot(gs[0, col_idx])
        ax_brain.set_facecolor('black')

        # Text axes (bottom row)
        ax_text = fig.add_subplot(gs[1, col_idx])
        ax_text.set_facecolor('black')
        ax_text.axis('off')

        visit_name = str(row['Visit']).upper()
        if visit_name in ['BL', 'SC']:
            visit_name = 'Baseline'

        raw_path  = os.path.join(ROOT_DIR, row['FilePath'])
        base_name = os.path.basename(raw_path).replace(".nii.gz", "").replace(".nii", "")
        seg_path  = os.path.join(os.path.dirname(raw_path), base_name + "_seg.nii.gz")

        if os.path.exists(raw_path) and os.path.exists(seg_path):

            # === 5. PLOT ZOOMED ROI INTO BRAIN AXES ===
            plotting.plot_roi(
                seg_path, bg_img=raw_path,
                display_mode='y', cut_coords=[0], axes=ax_brain,
                cmap='autumn', alpha=0.85,
                annotate=False, draw_cross=False, colorbar=False, dim=-0.5
            )

            # FIX 2: Y limit raised at the bottom so brain slice is not clipped
            # Brain content sits roughly -60 to +40 MNI; give 10mm breathing room each side
            ax_brain.set_ylim(-68, 50)
            ax_brain.set_xlim(-65, 65)

            # Title above brain
            ax_brain.set_title(
                f"{cls} Representative | {visit_name}
ID: {row['SubjectID']}",
                color='white', fontsize=13, fontweight='bold', pad=8
            )

            # L / R radiological labels (inside brain axes, safely within xlim/ylim)
            ax_brain.text(-57, 40, 'R', color='lightgray', fontsize=13,
                          fontweight='bold', ha='center', va='center')
            ax_brain.text( 57, 40, 'L', color='lightgray', fontsize=13,
                          fontweight='bold', ha='center', va='center')

            # FIX 3: Volume text goes into DEDICATED TEXT AXES — never clipped
            vol = row['Volume_mm3']
            ax_text.text(
                0.5, 0.55,
                f"★  HC Vol: {vol:,.0f} mm³",
                color=class_colors[cls],
                fontsize=15, fontweight='bold',
                ha='center', va='center',
                transform=ax_text.transAxes
            )

        else:
            ax_brain.text(0, 0, 'Image Missing', color='red', ha='center', va='center')
            ax_brain.set_ylim(-10, 10)
            ax_brain.set_xlim(-10, 10)
            ax_brain.axis('off')

    # === 6. OVERALL FIGURE TITLE ===
    fig.suptitle(
        "Representative Baseline Hippocampal Segmentations by Diagnostic Group",
        color='white', fontsize=14, fontweight='bold', y=1.01
    )

    # === 7. SAVE ===
    output_filename = '1x3_flowchart_brains_labeled.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight',
                facecolor='black', pad_inches=0.15)
    print(f"✅ Saved as '{output_filename}'")
    plt.show()


if __name__ == "__main__":
    generate_1x3_flowchart_brains()
