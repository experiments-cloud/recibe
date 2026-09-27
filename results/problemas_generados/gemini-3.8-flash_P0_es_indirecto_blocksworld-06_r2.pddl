(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
  )
  (:init
    (handempty)
    (clear f)
    (on f e)
    (on e b)
    (ontable b)
    (clear d)
    (on d a)
    (on a c)
    (ontable c)
  )
  (:goal
    (and
      (on c b)
      (on b a)
      (on a e)
      (on e f)
      (on f d)
    )
  )
)
