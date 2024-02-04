import java.awt.Color;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.awt.geom.RoundRectangle2D;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

import com.formdev.flatlaf.FlatDarculaLaf;
import java.awt.Toolkit;


////////////////////////////////////////////////////////////////////////////////-----------Fenetre Models------------///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

public class Models extends JFrame {
	

	private static final long serialVersionUID = 1L;

	
	Connection cnx=null;
	PreparedStatement prepared = null;
	ResultSet resultat =null; 
	
	private int posX = 0;   //Position X de la souris au clic
    private int posY = 0;   //Position Y de la souris au clic
    

	private JPanel contentPane;
	
	private int i=1; //deffiler les images
	
	private JTextArea testAreaDesc;
	private JScrollPane scrollpane; 
	private JScrollPane scrollpaneIMG; 

	

	/**
	 * Launch the application.
	 * @throws UnsupportedLookAndFeelException 
	 */
	public static void main(String[] args) throws UnsupportedLookAndFeelException {
		FlatDarculaLaf.install();	
		UIManager.setLookAndFeel(new FlatDarculaLaf() );
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Models frame = new Models("-1","NONE",false);
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	

	/**
	 * Create the frame.
	 */
	public Models(String dataset,String path_data,Boolean DataProcessed ) {
		setIconImage(Toolkit.getDefaultToolkit().getImage(Models.class.getResource("/Menu_img/model.png")));
		//cnx

		setUndecorated(true);	
		setResizable(false);

		setTitle("Models");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(0, 0, 1100, 650);
		setShape(new RoundRectangle2D.Double(0d, 0d, 1100d, 650d, 25d, 25d));
		setLocationRelativeTo(null);
		//vu que la frame est Undecorated on a besoin de ces MouseListeners pour la faire bouger(frame)
		  addMouseListener(new MouseAdapter() {
	            @Override
	            //on recupere les coordonnées de la souris
	            public void mousePressed(MouseEvent e) {
	                posX = e.getX();    //Position X de la souris au clic
	                posY = e.getY();    //Position Y de la souris au clic
	            }
	        });
	        addMouseMotionListener(new MouseMotionAdapter() {
	            // A chaque deplacement on recalcul le positionnement de la fenetre
	            @Override
	            public void mouseDragged(MouseEvent e) {
	                int depX = e.getX() - posX;
	                int depY = e.getY() - posY;
	                setLocation(getX()+depX, getY()+depY);
	            }
	        });
	        
	        
		contentPane = new JPanel();
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		scrollpaneIMG = new JScrollPane();
		scrollpaneIMG.setBounds(408, 112,  656, 446);
		scrollpaneIMG.setBorder(BorderFactory.createEmptyBorder());
		scrollpaneIMG.getViewport().setOpaque(false);
		contentPane.add(scrollpaneIMG);
		
		
// le BG et lannimation////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JLabel ModelsIMG = new JLabel("");
		scrollpaneIMG.setViewportView(ModelsIMG);
		ModelsIMG.setIcon(new ImageIcon(Models.class.getResource("/Models_img/1.PNG")));//animation de base;
		
		JLabel BGModels = new JLabel("");
		BGModels.setIcon(new ImageIcon(Models.class.getResource("/Models_img/BG 1.png")));
		//BGModels.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/1.png")));	// Back ground de base	
       
// Bouton Reduire ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JButton Minimise_BTN = new JButton("");
		Minimise_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/Minimize ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/Minimize ML .png")));
			}
		});
		Minimise_BTN.setToolTipText("Minimize");
		ButtonStyle(Minimise_BTN);
		Minimise_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setState(ICONIFIED);
				
			}
		});
		Minimise_BTN.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/Minimize ML .png")));
		Minimise_BTN.setBounds(932, 11, 32, 32);
		contentPane.add(Minimise_BTN);
//Boutton home//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				JButton btnHome = new JButton("");
				btnHome.addMouseListener(new MouseAdapter() {
					@Override
					public void mouseEntered(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(Models.class.getResource("/Models_img/home selected.png")));//changer les couleurs button
						}
					}
					@Override
					public void mouseExited(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(Models.class.getResource("/Models_img/home.png")));//remetre le bouton de base
						}
					}
				});
				btnHome.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
							Menu frame = new Menu(dataset,path_data,DataProcessed);
							frame.setLocationRelativeTo(null);
							frame.setVisible(true);
							dispose();
					}
				});
				btnHome.setIcon(new ImageIcon(Models.class.getResource("/Models_img/home.png")));
				btnHome.setToolTipText("Menu");
				btnHome.setBounds(974, 11, 32, 32);
				ButtonStyle(btnHome);
				contentPane.add(btnHome);
// Exit bouton//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		JButton Exit_BTN = new JButton("");
		Exit_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/Exit ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/Exit ML.png")));
			}
		});
		Exit_BTN.setToolTipText("Exit");
		ButtonStyle(Exit_BTN);
		Exit_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			
					
					int ClickedButton	=JOptionPane.showConfirmDialog(null, "Do you really want to leave?", "Close", JOptionPane.YES_NO_OPTION);
					if(ClickedButton==JOptionPane.YES_OPTION)
					{					
						dispose();
					}
					
					
			}
			
		});
		Exit_BTN.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/Exit ML.png")));
		Exit_BTN.setBounds(1016, 11, 32, 32);
		contentPane.add(Exit_BTN);
		
		
		
		JButton btnR = new JButton("");
		btnR.setIcon(new ImageIcon(Models.class.getResource("/Models_img/next.png")));
		btnR.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				btnR.setIcon(new ImageIcon(Models.class.getResource("/Models_img/next selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				btnR.setIcon(new ImageIcon(Models.class.getResource("/Models_img/next.png")));
			}
		});
		btnR.setToolTipText("Next");
		btnR.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				if (i==4)	i=0;
				if (i==5)	i=0;
				if (i<4) {
					i++;
					ModelsIMG.setIcon(new ImageIcon(Models.class.getResource("/Models_img/"+i+".PNG")));
					BGModels.setIcon(new ImageIcon(Models.class.getResource("/Models_img/BG "+i+".png")));
				}
				if(i==1)
				{
					testAreaDesc.setText("Cette figure  décrit l’architecture\n"
							+ " globale de notre approche de\n"
							+ " recommandation, qui propose\n"
							+ " une hybridation des algorithmes\n"
							+ " de FC et FBC avec l’information \n"
							+ "sociale, selon une architecture DL.");
				}
				if(i==2)
				{
					testAreaDesc.setText("Ce modèle est une hybridation\n"
							+ "du FC et FBC qui se charge\n"
							+ " de l’apprentissage de la fonction\n"
							+ " d’interaction afin de prédire\n"
							+ " la probabilité d’interaction\n"
							+ " entre l’utilisateur u et l’item i.");
					
				}
				if(i==3)
				{	testAreaDesc.setText("Le module SocHybMLP traite \n"
						+ "les deux aspects du filtrage \n"
						+ "social : l’amitié et la confiance.");
					
				}
				if(i==4)
				{
					testAreaDesc.setText("Ce module se charge de la\n"
							+ " combinaison des résultats \n"
							+ "des deux derniers modules afin\n"
							+ " de recommander des items \n"
							+ "pertinents à l’utilisateur \n"
							+ "sensible au contexte dans\n"
							+ " lequel il se trouve.\r\n" + 
							"");
				}
				
			}
		});
		btnR.setBounds(1066, 314, 32, 32);
		ButtonStyle(btnR);
		contentPane.add(btnR);
		
		JButton btnL = new JButton("");
		btnL.setIcon(new ImageIcon(Models.class.getResource("/Models_img/previous.png")));
		btnL.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				btnL.setIcon(new ImageIcon(Models.class.getResource("/Models_img/previous selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				btnL.setIcon(new ImageIcon(Models.class.getResource("/Models_img/previous.png")));
			}
		});
		btnL.setToolTipText("Previous");
		btnL.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				if (i==0)	i=4;
				if (i==1)	i=5;
				if (i>1) {
					i--;
					ModelsIMG.setIcon(new ImageIcon(Models.class.getResource("/Models_img/"+i+".PNG")));
					BGModels.setIcon(new ImageIcon(Models.class.getResource("/Models_img/BG "+i+".png")));
					if(i==1)
					{
						testAreaDesc.setText("Cette figure  décrit l’architecture\n"
								+ " globale de notre approche de\n"
								+ " recommandation, qui propose\n"
								+ " une hybridation des algorithmes\n"
								+ " de FC et FBC avec l’information \n"
								+ "sociale, selon une architecture DL.");
					}
					if(i==2)
					{
						testAreaDesc.setText("Ce modèle est une hybridation\n"
								+ "du FC et FBC qui se charge\n"
								+ " de l’apprentissage de la fonction\n"
								+ " d’interaction afin de prédire\n"
								+ " la probabilité d’interaction\n"
								+ " entre l’utilisateur u et l’item i.");
						
					}
					if(i==3)
					{	testAreaDesc.setText("Le module SocHybMLP traite \n"
							+ "les deux aspects du filtrage \n"
							+ "social : l’amitié et la confiance.");
						
					}
					if(i==4)
					{
						testAreaDesc.setText("Ce module se charge de la\n"
								+ " combinaison des résultats \n"
								+ "des deux derniers modules afin\n"
								+ " de recommander des items \n"
								+ "pertinents à l’utilisateur \n"
								+ "sensible au contexte dans\n"
								+ " lequel il se trouve.\r\n" + 
								"");
					}
					
				}
			}
		});
		btnL.setBounds(373, 314, 32, 32);
		ButtonStyle(btnL);
		contentPane.add(btnL);
		
		testAreaDesc = new JTextArea();
		testAreaDesc.setBackground(new Color(255, 51, 51));
		testAreaDesc.setForeground(Color.WHITE);
		testAreaDesc.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
		testAreaDesc.setText("Cette figure  décrit l’architecture\n"
				+ " globale de notre approche de\n"
				+ " recommandation, qui propose\n"
				+ " une hybridation des algorithmes\n"
				+ " de FC et FBC avec l’information \n"
				+ "sociale, selon une architecture DL.");
		testAreaDesc.setRows(10);
		testAreaDesc.setEditable(false);
		testAreaDesc.setSelectionStart(0);// le xceollpane affiche de haut en bas
		testAreaDesc.setSelectionEnd(0);
		testAreaDesc.setOpaque(false);
		testAreaDesc.setColumns(10);
	

		
		scrollpane = new JScrollPane(testAreaDesc);
		scrollpane.setBounds(96, 159, 260, 328);
		scrollpane.setBorder(BorderFactory.createEmptyBorder());
		scrollpane.getViewport().setOpaque(false);
		contentPane.add(scrollpane);
		
//le background////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		BGModels.setBounds(0, 0, 1100, 650);
		contentPane.add(BGModels);
		
	}
//methode du style des buttons/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	 private void ButtonStyle(JButton btn) {
	//enlecer les bordures des btn
	 btn.setOpaque(false);
	 btn.setFocusPainted(false);
	 btn.setBorderPainted(false);
	 btn.setContentAreaFilled(false);
	
}
}
