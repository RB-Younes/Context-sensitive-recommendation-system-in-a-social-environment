import java.awt.EventQueue;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.awt.geom.RoundRectangle2D;
import java.util.TimerTask;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

import com.formdev.flatlaf.FlatDarculaLaf;

////////////////////////////////////////////////////////////////////////////////-----------Fenetre Menu------------///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

public class Menu extends JFrame {
	

	private static final long serialVersionUID = 1L;

	private java.util.Timer chrono2 = new java.util.Timer();
	
	private int posX = 0;   //Position X de la souris au clic
    private int posY = 0;   //Position Y de la souris au clic
    

	private JPanel contentPane;
	

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
					Menu frame = new Menu("-1","NONE",false);
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
	public Menu(String dataset,String path_data,Boolean DataProcessed ) {
		setIconImage(Toolkit.getDefaultToolkit().getImage(Menu.class.getResource("/Menu_img/artificial-intelligence.png")));
		//cnx

		setUndecorated(true);	
		setResizable(false);
		//setIconImage(Toolkit.getDefaultToolkit().getImage(Menu.class.getResource("/Menu_img/medical-care.png")));
		setTitle("Menu");
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
		
		
// le BG et lannimation////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JLabel Docanimation1 = new JLabel("");
		Docanimation1.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/base animation.gif")));//animation de base
		chrono2 =new java.util.Timer();
		chrono2.schedule(new TimerTask() {
			@Override
			public void run() {
				Docanimation1.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/base animation looping.gif")));//animation looping
			}
		}, 1500);
		Docanimation1.setBounds(491, 173, 550, 417);
		contentPane.add(Docanimation1);
		
		JLabel BGMenu = new JLabel("");
		BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/1.png")));	// Back ground de base	
       
// Bouton Reduire ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JButton Minimise_BTN = new JButton("");
		Minimise_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/Minimize ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/Minimize ML .png")));
			}
		});
		Minimise_BTN.setToolTipText("Minimize");
		ButtonStyle(Minimise_BTN);
		Minimise_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setState(ICONIFIED);
				
			}
		});
		Minimise_BTN.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/Minimize ML .png")));
		Minimise_BTN.setBounds(932, 11, 32, 32);
		contentPane.add(Minimise_BTN);
// Exit bouton//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		JButton Exit_BTN = new JButton("");
		Exit_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/Exit ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/Exit ML.png")));
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
		Exit_BTN.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/Exit ML.png")));
		Exit_BTN.setBounds(1016, 11, 32, 32);
		contentPane.add(Exit_BTN);
//Boutton home//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JButton btnHome = new JButton("");
		btnHome.setEnabled(false);
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
		btnHome.setIcon(new ImageIcon(Models.class.getResource("/Models_img/home.png")));
		btnHome.setToolTipText("Menu");
		btnHome.setBounds(974, 11, 32, 32);
		ButtonStyle(btnHome);
		contentPane.add(btnHome);
		
		
//boutons P1///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
	//Model bouton***************************************************************************************************************************************************************************************************************************	
		JButton btnModels = new JButton();
			btnModels.setToolTipText("Models");
			btnModels.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent arg0) {
					chrono2.cancel();
					chrono2.purge();
					Models frame = new Models(dataset,path_data,DataProcessed);
					frame.setLocationRelativeTo(contentPane);
					frame.setVisible(true);
					dispose();
				}
			});
			btnModels.addMouseListener(new MouseAdapter() {
				@Override
				public void mouseEntered(MouseEvent e) {
					BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/2.png")));//changer le BackGround(arrière plan)	du menu pour faire un effet visuelle
					ImageIcon animationbtn1 =new ImageIcon(Menu.class.getResource("/Menu_img/models.gif"));	//animation Agenda
					animationbtn1.getImage().flush(); // réinitialiser l'animation
					chrono2.cancel();
					chrono2.purge();
					Docanimation1.setIcon(animationbtn1);
				}
				@Override
				public void mouseExited(MouseEvent e) {
					BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/1.png")));// remetre l'arriere plan de base (du debut)	
					ImageIcon animationBG =new ImageIcon(Menu.class.getResource("/Menu_img/base animation.gif"));	//animation de base
					chrono2 =new java.util.Timer();
					chrono2.schedule(new TimerTask() {
						@Override
						public void run() {
							Docanimation1.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/base animation looping.gif")));//animation looping
						}
					}, 1500);
					animationBG.getImage().flush(); // réinitialiser l'animation du menu de base
					Docanimation1.setIcon(animationBG);
				}
			});
			ButtonStyle(btnModels);
			btnModels.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/model.png")));
			btnModels.setBounds(81, 54, 128, 157);
			contentPane.add(btnModels);

			
	//dataset bouton*********************************************************************************************************************************************************************************************************************		
			JButton btnDatasets = new JButton("");
			btnDatasets.setToolTipText("Datasets");
			btnDatasets.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent arg0) {
					chrono2.cancel();
					chrono2.purge();
					Datasets frame = new Datasets(dataset,path_data,DataProcessed);
					frame.setLocationRelativeTo(contentPane);
					frame.setVisible(true);
					dispose();
				
				}
			});
			btnDatasets.addMouseListener(new MouseAdapter() {
				@Override
				public void mouseEntered(MouseEvent e) {
					BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/3.png")));//changer le BackGround(arrière plan)		
					ImageIcon animationbtn2 =new ImageIcon(Menu.class.getResource("/Menu_img/datasets.gif")); //animation 
					animationbtn2.getImage().flush(); // réinitialiser l'animation
					Docanimation1.setIcon(animationbtn2);
					chrono2.cancel();
					chrono2.purge();
				}
				@Override
				public void mouseExited(MouseEvent e) {
					BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/1.png")));// remetre l'arriere plan de base (du debut)	
					ImageIcon animationBG =new ImageIcon(Menu.class.getResource("/Menu_img/base animation.gif"));	//animation de base
					chrono2 =new java.util.Timer();
					chrono2.schedule(new TimerTask() {
						@Override
						public void run() {
							Docanimation1.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/base animation looping.gif")));//animation looping
						}
					}, 1500);
					animationBG.getImage().flush(); // réinitialiser l'animation du menu de base
					Docanimation1.setIcon(animationBG);
				}
			});
			ButtonStyle(btnDatasets);
			btnDatasets.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/data.png")));
			btnDatasets.setBounds(247, 147, 128, 157);
			contentPane.add(btnDatasets);
			
	//Training Medicaments*************************************************************************************************************************************************************************************************************************		
			JButton btnTraining = new JButton();
			btnTraining.setToolTipText("Training");
			btnTraining.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent arg0) {//ouverture de la fenetre  au clique
				if (DataProcessed== true) {
					chrono2.cancel();
					chrono2.purge();
					Training frame = new Training(dataset,path_data,DataProcessed);
					frame.setLocationRelativeTo(contentPane);
					frame.setVisible(true);
					dispose();
				}
				else {
					JOptionPane.showMessageDialog(null,  "Please process a dataset !","Warning" ,JOptionPane.PLAIN_MESSAGE, new ImageIcon(Datasets.class.getResource("/state/error.png")));	
				}
					
				}
			});
			btnTraining.addMouseListener(new MouseAdapter() {
				@Override
				public void mouseEntered(MouseEvent e) {
					BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/4.png")));	//changer le BackGround(arrière plan)		
					ImageIcon animationbtn3 =new ImageIcon(Menu.class.getResource("/Menu_img/Training.gif")); //animation 
					animationbtn3.getImage().flush(); // réinitialiser l'animation
					Docanimation1.setIcon(animationbtn3);
					chrono2.cancel();
					chrono2.purge();
				}
				@Override
				public void mouseExited(MouseEvent e) {
					BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/1.png")));// remetre l'arriere plan de base (du debut)	
					ImageIcon animationBG =new ImageIcon(Menu.class.getResource("/Menu_img/base animation.gif"));	//animation de base
					chrono2 =new java.util.Timer();
					chrono2.schedule(new TimerTask() {
						@Override
						public void run() {
							Docanimation1.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/base animation looping.gif")));//animation looping
						}
					}, 1500);
					animationBG.getImage().flush(); // réinitialiser l'animation du menu de base
					Docanimation1.setIcon(animationBG);
				}
			});
			ButtonStyle(btnTraining);
			btnTraining.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/train.png")));
			btnTraining.setBounds(81, 237, 128, 157);
			contentPane.add(btnTraining);
			
	//Tests & Results bouton*******************************************************************************************************************************************************************************************************************************		
			JButton btnTestResult = new JButton();
			btnTestResult.setToolTipText("Tests & Results");
			btnTestResult.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					chrono2.cancel();
					chrono2.purge();
					results frame = new results(dataset,path_data,DataProcessed);
					frame.setLocationRelativeTo(contentPane);
					frame.setVisible(true);
					dispose();
				}
			});
			btnTestResult.addMouseListener(new MouseAdapter() {
				@Override
				public void mouseEntered(MouseEvent e) {
					BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/5.png")));	//changer le BackGround(arrière plan)	
					ImageIcon animationbtn4 =new ImageIcon(Menu.class.getResource("/Menu_img/test&result.gif"));//animation 
					animationbtn4.getImage().flush(); // réinitialiser l'animation
					Docanimation1.setIcon(animationbtn4);
					chrono2.cancel();
					chrono2.purge();
				}
				@Override
				public void mouseExited(MouseEvent e) {
					BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/1.png")));// remetre l'arriere plan de base (du debut)	
					ImageIcon animationBG =new ImageIcon(Menu.class.getResource("/Menu_img/base animation.gif"));	//animation de base
					chrono2 =new java.util.Timer();
					chrono2.schedule(new TimerTask() {
						@Override
						public void run() {
							Docanimation1.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/base animation looping.gif")));//animation looping
						}
					}, 1500);
					animationBG.getImage().flush(); // réinitialiser l'animation du menu de base
					Docanimation1.setIcon(animationBG);
				}
			});
			ButtonStyle(btnTestResult);
			btnTestResult.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/test & result.png")));
			btnTestResult.setBounds(247, 333, 128, 157);
			contentPane.add(btnTestResult);
			
		// bouton****************************************************************************************************************************************************************************************************************		

			JButton btnAbout = new JButton();
			btnAbout.setToolTipText("About");
			btnAbout.addMouseListener(new MouseAdapter() {
				@Override
				public void mouseEntered(MouseEvent arg0) {
					BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/6.png")));	//changer le BackGround(arrière plan)
					ImageIcon animationbtn5 =new ImageIcon(Menu.class.getResource("/Menu_img/about.gif"));//animation 
					animationbtn5.getImage().flush(); // réinitialiser l'animation
					Docanimation1.setIcon(animationbtn5);
					chrono2.cancel();
					chrono2.purge();
				}
				@Override
				public void mouseExited(MouseEvent e) {
					BGMenu.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/1.png")));// remetre l'arriere plan de base (du debut)	
					ImageIcon animationBG =new ImageIcon(Menu.class.getResource("/Menu_img/base animation.gif"));	//animation de base
					chrono2 =new java.util.Timer();
					chrono2.schedule(new TimerTask() {
						@Override
						public void run() {
							Docanimation1.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/base animation looping.gif")));//animation looping
						}
					}, 1500);
					animationBG.getImage().flush(); // réinitialiser l'animation du menu de base
					Docanimation1.setIcon(animationBG);
				}
			});
			// enlever les bordures des buttons
			ButtonStyle(btnAbout);
			btnAbout.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent arg0) {//ouverture  au clique
					chrono2.cancel();
					chrono2.purge();
					About frame = new About(dataset,path_data,DataProcessed);
					frame.setLocationRelativeTo(contentPane);
					frame.setVisible(true);
					dispose();
					
				}
			});
			btnAbout.setIcon(new ImageIcon(Menu.class.getResource("/Menu_img/about.png")));
			btnAbout.setBounds(81, 422, 128, 157);
			contentPane.add(btnAbout);
		
//le background////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		BGMenu.setBounds(0, 0, 1100, 650);
		contentPane.add(BGMenu);
		
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
