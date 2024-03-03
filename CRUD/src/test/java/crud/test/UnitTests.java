package crud.test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import crud.entity.User;
import crud.repo.UserRepository;
import crud.service.UserService;

class UserControllerTest {

	@Mock
	private UserRepository userRepository;

	@InjectMocks
	private UserService userService;

	@BeforeEach
	void setUp() {
		MockitoAnnotations.initMocks(this);
	}

	@Test
	void testGetAllUsers() {
		List<User> userList = new ArrayList<>();
		userList.add(new User(1L, "John", "Doe"));
		userList.add(new User(2L, "Jane", "Smith"));

		when(userRepository.findAll()).thenReturn(userList);

		List<User> result = userService.getAllUsers();

		assertEquals(2, result.size());
		assertEquals("John", result.get(0).getFirstName());
		assertEquals("Jane", result.get(1).getFirstName());
	}

	@Test
	void testGetUserById() {
		User user = new User(1L, "John", "Doe");

		when(userRepository.findById(1L)).thenReturn(java.util.Optional.of(user));

		User result = userService.getUserById(1L);

		assertEquals("John", result.getFirstName());
		assertEquals("Doe", result.getLastName());
	}

	@Test
	void testCreateUser() {
		
		User newUser2 = new User(0, "Alice", "Johnson");
		User savedUser2 = new User(3L, "Alice", "Johnson");

		when(userRepository.save(newUser2)).thenReturn(savedUser2);

		User result = userService.createUser(newUser2);

		assertEquals(3L, result.getId());
		assertEquals("Alice", result.getFirstName());
		assertEquals("Johnson", result.getLastName());
	}

	@Test
	void testUpdateUser() {
		User existingUser = new User(1L, "John", "Doe");
		User updatedUser = new User(1L, "John", "Smith");

		when(userRepository.findById(1L)).thenReturn(java.util.Optional.of(existingUser));
		when(userRepository.save(updatedUser)).thenReturn(updatedUser);

		User result = userService.updateUser(1L, updatedUser);

		assertEquals("Smith", result.getLastName());
	}

	@Test
	void testDeleteUser() {
		userService.deleteUser(1L);

		verify(userRepository, times(1)).deleteById(1L);
	}

}
